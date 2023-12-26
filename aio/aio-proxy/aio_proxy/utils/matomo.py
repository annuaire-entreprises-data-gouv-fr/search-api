import asyncio
import hashlib
import logging
import os
import random
import time
import urllib

import requests
from dotenv import load_dotenv

load_dotenv()

ID_SITE = os.getenv("MATOMO_ID_SITE")
TRACKING_URL = os.getenv("MATOMO_TRACKING_URL")
# Probability of tracking the event (1 in 1000)
TRACKING_PROBABILITY = 1 / 1000


async def track_api_call_via_matomo(request):
    try:
        time.sleep(15)
        rec = 1  # Required for tracking
        url = f"https://recherche-entreprises.api.gouv.fr/{str(request.rel_url.query)}"
        action_name = "Recherche API"
        _id = generate_unique_visitor_id(request)

        tracking_params = {
            "idsite": ID_SITE,
            "rec": rec,
            "action_name": action_name,
            "url": url,
            "_id": _id,
            "apiv": 1,
        }

        tracking_data = urllib.parse.urlencode(tracking_params)
        tracking_url = TRACKING_URL + tracking_data
        requests.get(tracking_url)
    except Exception as error:
        logging.info(f"Matomo logging failed: {error}")


def generate_unique_visitor_id(request):
    ip_address = request.headers.get("X-Forwarded-For") or request.remote
    hashed_ip = hashlib.sha256(ip_address.encode("utf-8")).hexdigest()
    return hashed_ip


def track_event(request):
    random_number = random.random()
    if random_number < TRACKING_PROBABILITY:
        loop = asyncio.get_event_loop()
        return loop.create_task(track_api_call_via_matomo(request))
