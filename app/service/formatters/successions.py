from app.models.unite_legale import Succession, SuccessionEntry


def format_succession_entries(entries):
    if not entries:
        return None
    return [
        SuccessionEntry(
            siret=entry.get("siret"),
            date_lien_succession=entry.get("date_lien_succession"),
            transfert_siege=entry.get("transfert_siege"),
            continuite_economique=entry.get("continuite_economique"),
        )
        for entry in entries
    ]


def format_successions(source_successions):
    if not source_successions:
        return None
    return Succession(
        predecesseurs=format_succession_entries(
            source_successions.get("predecesseurs")
        ),
        successeurs=format_succession_entries(source_successions.get("successeurs")),
    )
