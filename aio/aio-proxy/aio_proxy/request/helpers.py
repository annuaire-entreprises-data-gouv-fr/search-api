from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(
    error="Veuillez indiquer une date minimale inférieure à la date maximale."
)
def validate_date_range(min_date=None, max_date=None):
    if min_date and max_date:
        if max_date < min_date:
            raise ValueError
