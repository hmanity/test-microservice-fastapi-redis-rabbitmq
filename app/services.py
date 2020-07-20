from aiohttp import ClientSession
from .core.config import settings


async def get_drugstores():
    async with ClientSession() as session:
        async with session.get(settings.ds_endpoint) as resp:
            drugstores = await resp.json()
            return [
                d["drugstore_id"]
                for d in drugstores["result"]
                if "drugstore_id" in d.keys()
            ]
