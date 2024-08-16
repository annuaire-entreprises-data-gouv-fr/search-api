import os
import pathlib

from dotenv import load_dotenv
from elasticsearch_dsl import connections
from fastapi import FastAPI

from app.router import router

load_dotenv()

# Get env variables
ENV = os.getenv("ENV")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_URL = os.getenv("ELASTIC_URL")
DSN_SENTRY = os.getenv("DSN_SENTRY")

# Connect to Elasticsearch
connections.create_connection(
    hosts=[ELASTIC_URL],
    http_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    retry_on_timeout=True,
)

app = FastAPI()

load_dotenv()

BASE_DIR = pathlib.Path(__file__).parent.parent
open_api_path = BASE_DIR / "aio_proxy" / "doc" / "open-api.yml"
ENV = os.getenv("ENV")

app = FastAPI(
    title="API Recherche d'entreprises",
    version="2.0.0",
    docs_url="/docs/",
    redoc_url="/redoc/",
)

# Include the router
app.include_router(router)
