from aio_proxy.response.helpers import serialize_error_text
from aiohttp import web

import elasticsearch


def http_exception_handler(func):
    """Handle bad request errors."""

    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (
            elasticsearch.exceptions.RequestError,
            ValueError,
            TypeError,
        ) as error:
            raise web.HTTPBadRequest(
                text=serialize_error_text(str(error)),
                content_type="application/json",
            )
        except BaseException as error:
            raise web.HTTPInternalServerError(
                text=serialize_error_text(str(error)),
                content_type="application/json",
            )

    return inner_function
