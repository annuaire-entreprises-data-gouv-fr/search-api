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
    terms = request.rel_url.query['q']
    page = request.rel_url.query.get('page', 1)
    page_size = request.rel_url.query.get('page_size', 20)
    res = search_es(Siren, terms, int(page), int(page_size))
    return web.Response(text=json.dumps(res, default=str))


@routes.get('/colors')
async def search_endpoint(request):
    return web.json_response({'CURRENT_COLOR': os.getenv('CURRENT_COLOR'), 'NEXT_COLOR': os.getenv('NEXT_COLOR')},
                             status=200)
