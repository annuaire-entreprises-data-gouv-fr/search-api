import json
import logging
import os
from urllib.request import urlopen

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)


def get_current_color(color_url):
    """Get current Elasticsearch index color from json file stored in MinIO."""
    try:
        with urlopen(color_url, timeout=5) as url:
            data = json.loads(url.read().decode())
            current_color = data["CURRENT_COLOR"]
            logging.info(
                f"******************** Current color from file: {current_color}"
            )
    except BaseException as error:
        logging.info(
            f"******************** Error getting file from MINIO:"
            f"{error}, using: blue as default!!!"
        )
        current_color = "blue"
    return current_color


CURRENT_COLOR = get_current_color(os.getenv("COLOR_URL"))
