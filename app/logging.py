import logging

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from app.config import CURRENT_ENV, DSN_SENTRY


def setup_logging():
    logging.basicConfig(level=logging.INFO)


def setup_sentry():
    if CURRENT_ENV == "prod":
        sentry_logging = LoggingIntegration(
            level=logging.INFO,
            event_level=logging.WARNING,
        )
        sentry_sdk.init(
            dsn=DSN_SENTRY,
            integrations=[
                FastApiIntegration(),
                sentry_logging,
            ],
            traces_sample_rate=0.01,
        )
