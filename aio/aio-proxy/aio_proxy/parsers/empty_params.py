from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(error="Veuillez indiquer au moins un paramètre de recherche.")
def check_empty_params(parameters):
    empty_parameters = all(param is None for param in parameters.values())
    if empty_parameters:
        raise ValueError
