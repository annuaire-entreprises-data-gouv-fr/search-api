import logging
import pathlib

import aiohttp
from aio_proxy.routes import routes
from aio_proxy.settings import config
from aiohttp_swagger import *
from aiohttp import web
from aiohttp_apispec import (docs,
                             request_schema,
                             response_schema,
                             setup_aiohttp_apispec)


BASE_DIR = pathlib.Path(__file__).parent.parent
swagger = BASE_DIR / "aio_proxy" / "doc" / "swagger.yml"


def main():
    logging.basicConfig(level=logging.DEBUG)

    app = web.Application()

    app["http_session"] = aiohttp.ClientSession()
    app.router.add_routes(routes)

    # setup_swagger(app, swagger_url="/doc", ui_version=2)
    setup_swagger(app,
                  swagger_url="/doc",
                  swagger_from_file=swagger,
                  )
    '''
    setup_aiohttp_apispec(app=app, title="My Documentation", version="v1",
                          swagger_path="/docs",)
    '''
    app["config"] = config
    web.run_app(app, host=config["host"], port=config["port"])
    app.on_startup.append(swagger)


if __name__ == "__main__":
    main()
