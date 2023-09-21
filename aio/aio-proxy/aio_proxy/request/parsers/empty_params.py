from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(error="Veuillez indiquer au moins un paramètre de recherche.")
def check_empty_params(parameters):
    # If all parameters are empty (except matching size and pagination
    # because they always have a default value) raise value error
    # Check if all non-default parameters are empty, raise a ValueError if they are
    non_default_params = [
        param_value
        for param, param_value in parameters.items()
        if param not in ["page", "per_page", "matching_size"]
    ]

    if all(val is None for val in non_default_params):
        raise ValueError
