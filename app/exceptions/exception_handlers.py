import logging
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from sentry_sdk import capture_exception, push_scope

from app.exceptions.exceptions import (
    InternalError,
    InvalidParamError,
    InvalidSirenError,
    NotFoundError,
    SearchApiError,
)


def create_exception_handler(
    status_code: int = 500, initial_detail: str = "Service is unavailable"
) -> Callable[[Request, SearchApiError], ORJSONResponse]:
    async def exception_handler(
        request: Request, exc: SearchApiError
    ) -> ORJSONResponse:
        detail = {
            "status_code": exc.status_code or status_code,
            "message": exc.message or initial_detail,
        }

        if isinstance(exc, InvalidParamError):
            with push_scope() as scope:
                scope.fingerprint = ["InvalidParamError"]
                logging.warning(f"Bad Request: {exc.message}")

        return ORJSONResponse(
            status_code=detail["status_code"],
            content={"erreur": detail["message"]},
        )

    return exception_handler


async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> ORJSONResponse:
    logging.error(f"Unhandled exception occurred: {exc}", exc_info=True)

    with push_scope() as scope:
        scope.set_context(
            "request",
            {
                "url": str(request.url),
                "method": request.method,
                "headers": dict(request.headers),
                "query_params": dict(request.query_params),
            },
        )
        capture_exception(exc)

    internal_error = InternalError(
        "Une erreur inattendue s'est produite. Veuillez réessayer plus tard."
    )

    handler = create_exception_handler()
    return await handler(request, internal_error)


def add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(InvalidSirenError, create_exception_handler())
    app.add_exception_handler(InvalidParamError, create_exception_handler())
    app.add_exception_handler(NotFoundError, create_exception_handler())
    app.add_exception_handler(Exception, unhandled_exception_handler)
