import os

import sentry_sdk
from aio_proxy.response.build_response import api_response
from aio_proxy.response.parameters import (
    extract_geo_parameters,
    extract_text_parameters,
)
from aio_proxy.search.search_functions import search_geo, search_text
from aiohttp import web
from dotenv import load_dotenv
from elasticsearch_dsl import connections
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from aio_proxy.search.helpers import CURRENT_COLOR

load_dotenv()

# Get env variables
ENV = os.getenv("ENV")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_URL = os.getenv("ELASTIC_URL")
DSN_SENTRY = os.getenv("DSN_SENTRY")

# Connect to Sentry in production
if ENV == "prod":
    sentry_sdk.init(dsn=DSN_SENTRY, integrations=[AioHttpIntegration()])

# Connect to Elasticsearch
connections.create_connection(
    hosts=[ELASTIC_URL],
    http_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    retry_on_timeout=True,
)

routes = web.RouteTableDef()


@routes.get("/search")
async def search_text_endpoint(request):
    return api_response(
        request, extract_function=extract_text_parameters, search_function=search_text
    )


@routes.get("/near_point")
async def near_point_endpoint(request):
    return api_response(
        request, extract_function=extract_geo_parameters, search_function=search_geo
    )
