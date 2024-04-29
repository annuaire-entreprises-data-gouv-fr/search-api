import asyncio
import logging
import os
import random
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
    # Generate a random hexadecimal string of length 16
    real_ip = request.headers.get("X-Real-Ip")
    forwarded_for = request.headers.get("X-Forwarded-For") or request.remote

    ip_address = (
        forwarded_for.split(",")[0].strip()
        if forwarded_for is not None and len(forwarded_for) > 0
        else real_ip
    )

    user_agent = request.headers.get("User-Agent")

    logging.info(
        f"X-Real-Ip: {real_ip} - X-Forwarded-For : {ip_address} - User-Agent : {user_agent}"
    )

    unique_id = f"{ip_address}|{user_agent}"
    hashed_id = hashlib.sha256(unique_id.encode("utf-8")).hexdigest()

    return hashed_id[:16]


def track_event(request):
    """
    Track an event based on a random probability.
    """
    random_number = random.random()
    if random_number < TRACKING_PROBABILITY:
        loop = asyncio.get_event_loop()
        return loop.create_task(track_api_call_via_matomo(request))
