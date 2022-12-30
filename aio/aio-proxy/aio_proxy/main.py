import logging
import pathlib

import aiohttp
from aio_proxy.routes import routes
from aio_proxy.settings import config
from aiohttp import web
from aiohttp_swagger3 import ReDocUiSettings, SwaggerDocs

BASE_DIR = pathlib.Path(__file__).parent.parent
open_api_path = BASE_DIR / "aio_proxy" / "doc" / "open-api.yml"


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
        version="1.0.0",
        components=open_api_path,
    )

    app["config"] = config
    web.run_app(app, host=config["host"], port=config["port"])
    app.on_startup.append(swagger)


if __name__ == "__main__":
    main()
