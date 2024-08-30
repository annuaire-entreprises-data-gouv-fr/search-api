import logging
from typing import Callable

import yaml
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from elasticsearch_dsl import connections
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from sentry_sdk import capture_exception, push_scope

from app.config import (
    APM_CONFIG,
    CURRENT_ENV,
    ELASTIC_PASSWORD,
    ELASTIC_URL,
    ELASTIC_USER,
    OPEN_API_PATH,
)
from app.exceptions.exceptions import (
    InternalError,
    InvalidParamError,
    InvalidSirenError,
    SearchApiError,
)
from app.logging import setup_logging, setup_sentry
from app.routers import admin, public

# Setup logging
setup_logging()

# Connect to Elasticsearch
connections.create_connection(
    hosts=[ELASTIC_URL],
    http_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    retry_on_timeout=True,
)

app = FastAPI(
    title="API Recherche d'entreprises",
    version="1.0.0",
    docs_url=None,
    redoc_url="/docs/",
)


# Load OpenAPI YAML file
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    logging.info(f"+++++++++++{OPEN_API_PATH}")
    with open(OPEN_API_PATH) as file:
        openapi_schema = yaml.safe_load(file)
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Sentry Integration and Elastic APM Integration for Production
if CURRENT_ENV == "prod":
    apm_client = make_apm_client(APM_CONFIG)
    app.add_middleware(ElasticAPM, client=apm_client)
    setup_sentry()

# Include routers
app.include_router(public.router)
app.include_router(admin.router)


def create_exception_handler(
    status_code: int = 500, initial_detail: str = "Service is unavailable"
) -> Callable[[Request, SearchApiError], ORJSONResponse]:
    # Using a dictionary to hold the detail
    detail = {"status_code": status_code, "message": initial_detail}

    async def exception_handler(
        request: Request, exc: SearchApiError
    ) -> ORJSONResponse:
        if exc.message:
            detail["message"] = exc.message

        if exc.status_code:
            detail["status_code"] = exc.status_code
        if isinstance(exc, InvalidParamError):
            with push_scope() as scope:
                scope.fingerprint = ["TESTING"]
                logging.warning(f"InvalidParamError: {exc.message}")
        return ORJSONResponse(
            status_code=detail["status_code"],
            content={"status_code": detail["status_code"], "detail": detail["message"]},
        )

    return exception_handler


app.add_exception_handler(
    exc_class_or_status_code=InvalidSirenError,
    handler=create_exception_handler(),
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidParamError,
    handler=create_exception_handler(),
)


# Add a catch-all exception handler for any unhandled exceptions
@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> ORJSONResponse:
    # Log the full exception details
    logging.error(f"Unhandled exception occurred: {exc}", exc_info=True)

    # Use Sentry to capture the exception
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

    # Create an InternalError with a generic message
    internal_error = InternalError(
        "Une erreur inattendue s'est produite. Veuillez réessayer plus tard."
    )

    # Use the create_exception_handler to handle the InternalError
    handler = create_exception_handler()
    return await handler(request, internal_error)
