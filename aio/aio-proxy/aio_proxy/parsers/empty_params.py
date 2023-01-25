from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(error="Veuillez indiquer au moins un paramètre de recherche.")
def check_empty_params(parameters):
    # If all parameters are empty (except matching size because it always has a
    # default value) raise value error
    empty_parameters = all(
        val is None
        for val in [parameters[x] for x in parameters if x != "matching_size"]
    )
    if empty_parameters:
        raise ValueError
