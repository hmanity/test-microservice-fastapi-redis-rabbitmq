from pydantic import BaseSettings  # pylint: disable=no-name-in-module


class Settings(BaseSettings):
    mongodb_dsn: str 
    mongo_max_connection: int = 1000
    mongo_min_connections: int = 10
    rmq_host: str 
    redis_dsn: str
    ourl: str = "/api/v2/inventories/docs/v1/openapi.json"
    timeout: int = 5
    sentry_dsn: str 
    ds_endpoint: str

    class Config:
        env_file = ".env"
        env_prefix = "APP_"


settings = Settings()
