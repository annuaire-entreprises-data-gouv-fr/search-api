import csv
import io
import logging
import threading

import requests

from app.config import settings
from app.elastic.es_index import StructureMapping
from app.elastic.parsers.siren import is_siren

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT_SECONDS = 10


def parse_siren_protege_csv(content: str) -> frozenset[str]:
    reader = csv.DictReader(io.StringIO(content))
    if reader.fieldnames is None or "siren" not in reader.fieldnames:
        raise ValueError("missing 'siren' column")

    sirens = set()
    for row in reader:
        siren = (row["siren"] or "").strip()
        if is_siren(siren):
            sirens.add(siren)
        else:
            logger.warning(f"Ignoring invalid SIREN in siren_protege list: {siren!r}")
    return frozenset(sirens)


def find_sirens_indexed_as_protege(sirens: frozenset[str]) -> frozenset[str]:
    if not sirens:
        return frozenset()
    search = (
        StructureMapping.search()
        .filter("terms", **{"unite_legale.siren": sorted(sirens)})
        .filter("term", **{"unite_legale.est_protege": True})
        .source(["unite_legale.siren"])
    )
    return frozenset(hit.unite_legale.siren for hit in search.scan())


class SirenProtegeList:
    """In-memory list of protected SIREN, refreshed periodically.

    The Elasticsearch index carries `unite_legale.est_protege`, but it is only
    rebuilt once a day while the list changes every hour: this list covers the
    gap. On a failed refresh, the last known list is kept.

    Search queries only need the SIREN not yet flagged in the index, usually a
    handful: sending the whole list in every query would weigh on latency.
    """

    def __init__(self, url: str, refresh_interval_seconds: int):
        self.url = url
        self.refresh_interval_seconds = refresh_interval_seconds
        self._sirens: frozenset[str] = frozenset()
        # Sorted once per refresh so that ES queries, and therefore their
        # cache keys, are identical across instances
        self._sirens_not_flagged_in_index: tuple[str, ...] = ()
        self._has_loaded = False
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def __contains__(self, siren: object) -> bool:
        return siren in self._sirens

    @property
    def sirens_not_flagged_in_index(self) -> tuple[str, ...]:
        return self._sirens_not_flagged_in_index

    def set_sirens(
        self,
        sirens: frozenset[str],
        sirens_flagged_in_index: frozenset[str] = frozenset(),
    ) -> None:
        self._sirens = sirens
        self._sirens_not_flagged_in_index = tuple(
            sorted(sirens - sirens_flagged_in_index)
        )

    def refresh(self) -> bool:
        try:
            response = requests.get(self.url, timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            sirens = parse_siren_protege_csv(response.text)
        except (requests.RequestException, ValueError) as error:
            logger.error(
                f"Could not refresh siren_protege list, keeping the "
                f"{len(self._sirens)} SIREN already loaded: {error}"
            )
            return False

        try:
            sirens_flagged_in_index = find_sirens_indexed_as_protege(sirens)
        except Exception as error:
            # Safe fallback: every SIREN of the list is filtered in queries
            logger.error(f"Could not check siren_protege against the index: {error}")
            sirens_flagged_in_index = frozenset()

        previous_sirens = self._sirens
        previous_not_flagged = self._sirens_not_flagged_in_index
        self.set_sirens(sirens, sirens_flagged_in_index)

        added = len(sirens - previous_sirens)
        removed = len(previous_sirens - sirens)
        not_flagged_changed = self._sirens_not_flagged_in_index != previous_not_flagged
        if not self._has_loaded or added or removed or not_flagged_changed:
            logger.info(
                f"siren_protege list updated: {len(sirens)} SIREN "
                f"(+{added} / -{removed}), "
                f"{len(self._sirens_not_flagged_in_index)} not yet flagged in the index"
            )
        self._has_loaded = True
        return True

    def start(self) -> None:
        self.refresh()
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._refresh_periodically, name="siren-protege", daemon=True
        )
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=REQUEST_TIMEOUT_SECONDS)
            self._thread = None

    def _refresh_periodically(self) -> None:
        while not self._stop_event.wait(self.refresh_interval_seconds):
            self.refresh()


siren_protege_list = SirenProtegeList(
    url=str(settings.siren_protege.url),
    refresh_interval_seconds=settings.siren_protege.refresh_interval_seconds,
)


def is_siren_protege(unite_legale: dict) -> bool:
    return (
        bool(unite_legale.get("est_protege"))
        or unite_legale.get("siren") in siren_protege_list
    )
