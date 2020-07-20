from typing import List

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Path
from pydantic.networks import import_email_validator

from .db.redis import Redis, get_pipe, get_redis
from .models import (Balancelist, Inventories, InventoriesSerializer,
                     Preorderlist, Pricelist)
from .mq import rabbitmq as rmq
from .services import get_drugstores
from .tasks import add_update_tasks

router = APIRouter()


@router.get(
    "/{product_id}",
    response_model=InventoriesSerializer.response_model,
    status_code=200,
)  # pylint: disable=maybe-no-member
async def get_inventory(
        *,
        product_id: str = Path(..., min_length=9),
        pipe=Depends(get_pipe),
        drugstores=Depends(get_drugstores, use_cache=True),
):
    for key in [f"{product_id}:{d}" for d in drugstores]:
        pipe.hgetall(key, encoding="utf-8")
    inv = Inventories(id=product_id)
    inv.inventorylist = [
        i for i in (await pipe.execute()) if i.get("drugstore_id")
    ]

    return inv


@router.post("/pricelist")
async def update_pricelist(
        *,
        tasks: BackgroundTasks,
        pricelist: List[Pricelist] = Body(..., embed=True),
        pool: rmq.Pool = Depends(rmq.get_channels_pool),
        redis: Redis = Depends(get_redis),
):
    await add_update_tasks(tasks, pricelist, redis, pool)


@router.post("/balancelist")
async def update_balancelist(
        *,
        tasks: BackgroundTasks,
        balancelist: List[Balancelist] = Body(..., embed=True),
        pool: rmq.Pool = Depends(rmq.get_channels_pool),
        redis: Redis = Depends(get_redis),
):
    await add_update_tasks(tasks, balancelist, redis, pool)


@router.post("/preorderlist")
async def update_preorder(
        *,
        tasks: BackgroundTasks,
        preorderlist: List[Preorderlist] = Body(..., embed=True),
        pool: rmq.Pool = Depends(rmq.get_channels_pool),
        redis: Redis = Depends(get_redis),
):
    await add_update_tasks(tasks, preorderlist, redis, pool)
