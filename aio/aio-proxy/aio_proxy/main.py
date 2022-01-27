import logging

import aiohttp
from aiohttp import web

from aio_proxy.routes import routes
from aio_proxy.settings import config


def main():
    logging.basicConfig(level=logging.DEBUG)

    app = web.Application()
    
    app['http_session'] = aiohttp.ClientSession()
    app.router.add_routes(routes)

    app['config'] = config
    web.run_app(app,
                host=config['host'],
                port=config['port'])


if __name__ == '__main__':
    main()
