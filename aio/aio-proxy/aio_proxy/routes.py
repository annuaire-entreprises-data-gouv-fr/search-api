import logging
import os

import sentry_sdk
from aiohttp import web
from dotenv import load_dotenv
from elasticsearch_dsl import connections
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from aio_proxy.request.search_type import SearchType
from aio_proxy.response.build_api_response import build_api_response
from aio_proxy.response.metadata_endpoint.convention_collective import (
    get_metadata_cc_response,
)

load_dotenv()

# Get env variables
ENV = os.getenv("ENV")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_URL = os.getenv("ELASTIC_URL")
DSN_SENTRY = os.getenv("DSN_SENTRY")

# Connect to Sentry in production
if ENV == "prod":
    sentry_logging = LoggingIntegration(
        level=logging.INFO,  # Capture info and above as breadcrumbs
        event_level=logging.WARNING,  # Send warnings as events
    )
    sentry_sdk.init(
        dsn=DSN_SENTRY,
        integrations=[
            AioHttpIntegration(transaction_style="method_and_path_pattern"),
            sentry_logging,
        ],
        # Log 10% of transactions for performance monitoring
        traces_sample_rate=0.1,
    )

# Connect to Elasticsearch
connections.create_connection(
    hosts=[ELASTIC_URL],
    http_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    retry_on_timeout=True,
)

routes = web.RouteTableDef()


@routes.get("/search")
async def search_text_endpoint(request):
    return build_api_response(
        request,
        search_type=SearchType.TEXT,
    )


@routes.get("/near_point")
async def near_point_endpoint(request):
    return build_api_response(
        request,
        search_type=SearchType.GEO,
    )


@routes.get("/metadata/conventions_collectives")
async def conventions_collectives_endpoint(request):
    """
    Endpoint for serving the convention collective JSON file.
    """
    return get_metadata_cc_response()
