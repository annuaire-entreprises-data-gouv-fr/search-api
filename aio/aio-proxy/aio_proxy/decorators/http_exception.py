import logging

from aio_proxy.response.helpers import serialize_error_text
from aiohttp import web
from pydantic import ValidationError
from sentry_sdk import capture_exception, push_scope

import elasticsearch


def http_exception_handler(func):
    """Handle errors and log them in Sentry."""

    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except elasticsearch.exceptions.RequestError as error:
            raise web.HTTPBadRequest(
                text=serialize_error_text(str(error)),
                content_type="application/json",
            )
        except ValidationError as err:
            with push_scope() as scope:
                # group value errors together based on their response
                # (Bad request)
                scope.fingerprint = ["Bad Request"]
                # capture_exception(error)
                logging.warning(
                    f"Bad Request: {err.errors()[0]['msg'].split(', ', 1)[1]}"
                )
                raise web.HTTPBadRequest(
                    text=serialize_error_text(
                        str(err.errors()[0]["msg"].split(", ", 1)[1])
                    ),
                    content_type="application/json",
                )
        except BaseException as error:
            # capture error in Sentry
            capture_exception(error)
            raise web.HTTPInternalServerError(
                text=serialize_error_text(str(error)),
                content_type="application/json",
            )

    return inner_function
