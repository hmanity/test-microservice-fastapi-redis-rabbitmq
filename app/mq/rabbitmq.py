import aio_pika
from aio_pika import ExchangeType, Message
from aio_pika.connection import Channel, Connection
from aio_pika.pool import Pool

from ..core.config import settings


class MQ:
    connection: Connection
    connections_pool: Pool
    channels_pool: Pool


rmq = MQ()


async def get_connection_rmq() -> Connection:
    return await aio_pika.connect_robust(host=settings.rmq_host, timeout=10)


async def get_channel() -> Channel:
    async with rmq.connections_pool.acquire() as connection:
        return await connection.channel()


async def get_channels_pool() -> Pool:
    return rmq.channels_pool


async def send_msg(pool: Pool, rk: str, msg: Message):
    async with pool.acquire() as channel:
        exchange = rk.split(".")[0]
        topic_exchange = await channel.declare_exchange(exchange, ExchangeType.TOPIC)
        await topic_exchange.publish(msg, routing_key=rk)
