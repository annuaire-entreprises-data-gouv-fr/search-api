from typing import List, Union, Any

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
    page = int(request.rel_url.query.get('page', 1)) - 1
    per_page = int(request.rel_url.query.get('page_size', 10))
    total_results, unite_legale = search_es(Siren, terms, page*per_page, per_page)
    res = {}
    res['unite_legale'] = unite_legale
    res['total_results'] = int(total_results)
    res['page'] = page + 1
    res['per_page'] = per_page
    res['total_pages'] = int(res['total_results']/res['per_page']) + 1
    return web.Response(text=json.dumps([res], default=str))


@routes.get('/colors')
async def search_endpoint(request):
    return web.json_response({'CURRENT_COLOR': os.getenv('CURRENT_COLOR'), 'NEXT_COLOR': os.getenv('NEXT_COLOR')},
                             status=200)
