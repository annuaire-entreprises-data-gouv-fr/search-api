import elasticsearch
from aio_proxy.helpers import serialize_error_text
from aiohttp import web


def http_exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (elasticsearch.exceptions.RequestError, ValueError, TypeError) as error:
            raise web.HTTPBadRequest(
                text=serialize_error_text(str(error)), content_type="application/json"
            )
        except BaseException as error:
            raise web.HTTPInternalServerError(
                text=serialize_error_text(str(error)), content_type="application/json"
            )

    return inner_function
