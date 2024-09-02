import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

# Environment variables
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_URL = os.getenv("ELASTIC_URL")
DSN_SENTRY = os.getenv("DSN_SENTRY")

# Other configuration constants
CURRENT_ENV = os.getenv("CURRENT_ENV", "dev")
APM_URL = os.getenv("APM_URL")
BASE_DIR = pathlib.Path(__file__).parent
OPEN_API_PATH = BASE_DIR / "doc" / "open-api.yml"


# Elastic APM configuration
APM_CONFIG = {
    "SERVICE_NAME": "SEARCH APM",
    "SERVER_URL": APM_URL,
    "ENVIRONMENT": CURRENT_ENV,
}
