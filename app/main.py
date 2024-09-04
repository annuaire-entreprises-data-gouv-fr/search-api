import yaml
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from elasticsearch_dsl import connections
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from app.config import (
    APM_CONFIG,
    CURRENT_ENV,
    ELASTIC_PASSWORD,
    ELASTIC_URL,
    ELASTIC_USER,
    OPEN_API_PATH,
)
from app.exceptions.exception_handlers import add_exception_handlers
from app.exceptions.exceptions import (
    NotFoundError,
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

# Add exception handlers
add_exception_handlers(app)


# Redirect /docs to /docs/
@app.get("/docs", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs/")


# Catch-all route for 404 errors
@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path_name: str):
    raise NotFoundError()