import logging

from fastapi.responses import ORJSONResponse
from pydantic import ValidationError
from sentry_sdk import capture_exception, push_scope

import elasticsearch
from app.exceptions.siren import InvalidSirenError
from app.response.helpers import serialize_error_text


def http_exception_handler(func):
    """Handle errors and log them in Sentry."""

    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as err:
            with push_scope() as scope:
                # group value errors together based on their response
                # (Bad request)
                scope.fingerprint = ["Bad Request"]
                # capture_exception(error)
                logging.warning(
                    f"Bad Request: {err.errors()[0]['msg'].split(', ', 1)[1]}"
                )
                return ORJSONResponse(
                    status_code=400,
                    content=serialize_error_text(
                        str(err.errors()[0]["msg"].split(", ", 1)[1])
                    ),
                )
        except (elasticsearch.exceptions.RequestError, InvalidSirenError) as error:
            return ORJSONResponse(
                status_code=400,
                content={"erreur": error.message},
            )
        except BaseException as error:
            # capture error in Sentry
            capture_exception(error)
            return ORJSONResponse(
                status_code=500,
                content=serialize_error_text(str(error)),
            )

    return inner_function
