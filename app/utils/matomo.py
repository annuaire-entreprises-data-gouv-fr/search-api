import asyncio
import hashlib
import logging
import random
import secrets
import urllib

import requests
from fastapi import Request

from app.config import settings

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
        relative_url = request.url.path + "?" + request.url.query
        url = f"https://recherche-entreprises.api.gouv.fr{str(relative_url)}"
        action_name = "Recherche API"
        _id = generate_unique_visitor_id(request)

        tracking_params = {
            "idsite": settings.matomo.id_site,
            "rec": rec,
            "action_name": action_name,
            "url": url,
            "uid": _id,
            "_id": _id,
            "apiv": 1,
        }

        tracking_data = urllib.parse.urlencode(tracking_params)
        tracking_url = str(settings.matomo.tracking_url) + tracking_data
        await requests.get(tracking_url, timeout=timeout)
    except Exception as error:
        logging.info(f"Matomo logging failed: {error}")


def generate_unique_visitor_id(request: Request):
    """
    This function extracts the IP address and user-agent from an HTTP request to create
    a unique identifier for tracking visitors on Matomo.
    """
    real_ip = request.headers.get("X-Real-Ip")
    forwarded_for = request.headers.get("X-Forwarded-For") or request.client.host

    ip_address = (
        forwarded_for.split(",")[0].strip()
        if forwarded_for is not None and len(forwarded_for) > 0
        else real_ip
    )

    user_agent = request.headers.get("User-Agent")

    unique_id = (
        f"{ip_address}|{user_agent}"
        if ip_address is not None or user_agent is not None
        else secrets.token_hex(8)
    )

    hashed_id = hashlib.sha256(unique_id.encode("utf-8")).hexdigest()[:16]

    logging.info(
        f"hashed_id: {hashed_id} - unique_id : {unique_id} - X-Real-Ip: {real_ip} "
        f"- X-Forwarded-For : {forwarded_for} - User-Agent : {user_agent}"
    )

    return hashed_id


def track_event(request: Request):
    """
    Track an event based on a random probability.
    """
    random_number = random.random()
    if random_number < TRACKING_PROBABILITY:
        loop = asyncio.get_event_loop()
        return loop.create_task(track_api_call_via_matomo(request))
