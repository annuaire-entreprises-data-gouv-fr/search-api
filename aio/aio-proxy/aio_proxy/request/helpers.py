from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(
    error="Veuillez indiquer une date minimale inférieure à la date maximale."
)
def validate_date_range(min_date=None, max_date=None):
    if min_date and max_date:
        if max_date < min_date:
            raise ValueError


MAX_RESULTS = 10000


@value_exception_handler(
    error="Le nombre total de résultats est restreint à 10 000. Pour garantir cela, "
    "le produit du numéro de page (par défaut, page = 1) et du nombre de résultats "
    "par page (par défaut, per_page = 10), c'est-à-dire `page * per_page`, ne doit pas "
    "excéder 10 000."
)
def validate_results_window(page=1, per_page=10):
    if page * per_page > MAX_RESULTS:
        raise ValueError
