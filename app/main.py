from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi_contrib.common.responses import UJSONResponse

from .core.config import settings
from .db.redis_utils import connect_to_redis
from .middlewares import middleware
from .mq.rabbitmq_utils import connect_to_rabbit, close_connections_to_rabbit
from .routers import router

app = FastAPI(default_response_class=UJSONResponse, middleware=middleware)

app.add_event_handler("startup", connect_to_rabbit)
app.add_event_handler("startup", connect_to_redis)
app.add_event_handler("shutdown", close_connections_to_rabbit)

@app.get("/ping")
async def ping():
    return "OK"


@app.get("/api/v2/inventories/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title + " - Swagger UI")


app.include_router(
    router, prefix="/api/v2/inventories", tags=["inventories"], responses={404: {"description": "Not found"}},
)
