import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware import Middleware

from .core.config import settings

sentry_sdk.init(dsn=settings.sentry_dsn,
                traces_sample_rate=1.0,
                _experiments={"auto_enabling_integrations": True})

middleware = [Middleware(SentryAsgiMiddleware)]
