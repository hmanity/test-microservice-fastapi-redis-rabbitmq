from ..db.redis import Redis
from ..models import BaseList


async def upsert_inventories(r: Redis, l: BaseList):
    pipe = r.pipeline()
    for item in l:
        key = f"{l.id}:{item.drugstore_id}"
        val = item.dict()
        pipe.hmset_dict(key, val)
    await pipe.execute()
