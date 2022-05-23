import elasticsearch
from aio_proxy.helpers import serialize_error_text
from aiohttp import web

headers = {"Access-Control-Allow-Origin": "*"}


def http_exception_handler(func):
    """Handle bad request errors."""

    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (elasticsearch.exceptions.RequestError, ValueError, TypeError) as error:
            raise web.HTTPBadRequest(
                text=serialize_error_text(str(error)),
                content_type="application/json",
                headers=headers,
            )
        except BaseException as error:
            raise web.HTTPInternalServerError(
                text=serialize_error_text(str(error)),
                content_type="application/json",
                headers=headers,
            )

    return inner_function
