from typing import List

from fastapi import BackgroundTasks

from .crud.inventories import upsert_inventories
from .models import BaseListT
from .mq import rabbitmq as rmq


async def add_update_tasks(tasks: BackgroundTasks, lists: List[BaseListT], r,
                           p):
    for l in lists:
        e_name = l.get_exchange()
        exchange = f"inventories.{e_name}.updated"
        tasks.add_task(upsert_inventories, r, l)
        tasks.add_task(rmq.send_msg, p, exchange, l.get_msg())
