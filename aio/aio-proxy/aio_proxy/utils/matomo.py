import asyncio
import hashlib
import logging
import os
import random
import secrets
import urllib

import requests
from dotenv import load_dotenv

load_dotenv()

ID_SITE = os.getenv("MATOMO_ID_SITE")
TRACKING_URL = os.getenv("MATOMO_TRACKING_URL")
# Probability of tracking the event (1 in 100)
TRACKING_PROBABILITY = 1 / 100


async def track_api_call_via_matomo(request, timeout=5):
    """
    Track an API call via Matomo.

    Args:
        request: The web request object.

    Raises:
        Exception: If Matomo logging fails, an exception is caught and logged.

    Notes:
        This function tracks the API call with Matomo using
        the provided request information, and the data is sent asynchronously.

    """
    try:
        rec = 1  # Required for tracking
        url = f"https://recherche-entreprises.api.gouv.fr{str(request.rel_url)}"
        action_name = "Recherche API"
        _id = generate_unique_visitor_id(request)

        tracking_params = {
            "idsite": ID_SITE,
            "rec": rec,
            "action_name": action_name,
            "url": url,
            "uid": _id,
            "_id": _id,
            "apiv": 1,
        }

        tracking_data = urllib.parse.urlencode(tracking_params)
        tracking_url = TRACKING_URL + tracking_data
        requests.get(tracking_url, timeout=timeout)
    except Exception as error:
        logging.info(f"Matomo logging failed: {error}")


def generate_unique_visitor_id(request):
    ip_address = request.headers.get("X-Forwarded-For") or request.remote
    if ip_address is None:
        return secrets.token_hex(8)  # Generate a random hexadecimal string of length 16
    hashed_ip = hashlib.sha256(ip_address.encode("utf-8")).hexdigest()
    return hashed_ip[:16]


def track_event(request):
    """
    Track an event based on a random probability.
    """
    random_number = random.random()
    if random_number < TRACKING_PROBABILITY:
        loop = asyncio.get_event_loop()
        return loop.create_task(track_api_call_via_matomo(request))
