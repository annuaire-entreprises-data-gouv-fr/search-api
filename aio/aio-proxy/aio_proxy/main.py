import logging
import os
import pathlib

import aiohttp
from aiohttp import web
from aiohttp_swagger3 import ReDocUiSettings, SwaggerDocs
from dotenv import load_dotenv
from elasticapm.contrib.aiohttp import ElasticAPM

from aio_proxy.response.helpers import APM_URL, CURRENT_ENV
from aio_proxy.routes import routes
from aio_proxy.settings import config

load_dotenv()

BASE_DIR = pathlib.Path(__file__).parent.parent
open_api_path = BASE_DIR / "aio_proxy" / "doc" / "open-api.yml"
ENV = os.getenv("ENV")


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("********Starting API")

    app = web.Application()

    app["http_session"] = aiohttp.ClientSession()
    app.router.add_routes(routes)
    swagger = SwaggerDocs(
        app,
        redoc_ui_settings=ReDocUiSettings(path="/docs/"),
        title="API Recherche d’entreprises",
        version="2.0.0",
        components=open_api_path,
    )
    app["config"] = config
    if ENV != "dev":
        app["ELASTIC_APM"] = {
            "SERVICE_NAME": "SEARCH APM",
            "SERVER_URL": APM_URL,
            "ELASTIC_APM_ENVIRONMENT": CURRENT_ENV,
        }
        ElasticAPM(app)
    web.run_app(app, host=config["host"], port=config["port"])
    app.on_startup.append(swagger)


if __name__ == "__main__":
    main()
