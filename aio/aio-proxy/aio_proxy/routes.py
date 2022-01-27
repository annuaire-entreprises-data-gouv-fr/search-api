from aiohttp import web
import os
import logging
from aio_proxy.index import Siren
import aio_proxy.secrets
from elasticsearch_dsl import connections
import json
from aio_proxy.search_functions import search_es
from aio_proxy import secrets

connections.create_connection(hosts=[secrets.ELASTIC_URL], http_auth=(secrets.ELASTIC_USER, secrets.ELASTIC_PASSWORD),
                              retry_on_timeout=True)

routes = web.RouteTableDef()


@routes.get('/search')
async def search_endpoint(request):
    terms = request.rel_url.query['query']
    res = search_es(Siren, terms)
    return web.Response(text=json.dumps(res, default=str))


@routes.get('/colors')
async def search_endpoint(request):
    return web.json_response({'CURRENT_COLOR': os.getenv('CURRENT_COLOR'), 'NEXT_COLOR': os.getenv('NEXT_COLOR')},
                             status=200)
