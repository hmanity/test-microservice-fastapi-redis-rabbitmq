from pydantic import BaseSettings  # pylint: disable=no-name-in-module


class Settings(BaseSettings):
    mongodb_dsn: str = "mongodb://admin:admin@10.42.0.26:27017"
    mongo_max_connection: int = 1000
    mongo_min_connections: int = 10
    rmq_host: str = "10.42.0.26"
    redis_dsn: str = "redis://10.42.0.26:7001/10"
    ourl: str = "/api/v2/inventories/docs/v1/openapi.json"
    timeout: int = 5
    sentry_dsn: str = "https://ddbd593caa8940a58d903ae84847189a@o420145.ingest.sentry.io/5337840"
    ds_endpoint: str = "https://api.etabl.ru/api/v2/drugstores"

    class Config:
        env_file = ".env"
        env_prefix = "APP_"


settings = Settings()
