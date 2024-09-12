import logging

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from app.config import settings


def setup_logging():
    logging.basicConfig(level=logging.INFO)


def setup_sentry():
    if settings.env == "prod":
        sentry_logging = LoggingIntegration(
            level=logging.INFO,
            event_level=logging.WARNING,
        )
        sentry_sdk.init(
            dsn=settings.sentry.dsn,
            integrations=[
                FastApiIntegration(),
                sentry_logging,
            ],
            traces_sample_rate=0.01,
        )
