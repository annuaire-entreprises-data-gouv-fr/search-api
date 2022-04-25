def value_exception_handler(error):
    def decorator(func):
        def inner_function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (TypeError, KeyError, ValueError):
                raise ValueError(str(error))

        return inner_function

    return decorator
