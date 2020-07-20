from aio_pika.pool import Pool

from .rabbitmq import get_channel, get_connection_rmq, rmq


async def connect_to_rabbit():
    rmq.connections_pool = Pool(get_connection_rmq, max_size=2)
    rmq.channels_pool = Pool(get_channel, max_size=10)


async def close_connections_to_rabbit():
    await rmq.connections_pool.close()
