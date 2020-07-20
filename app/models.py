from datetime import datetime
from typing import List, Optional, Sequence, TypeVar, Union

from aio_pika.message import Message
from fastapi_contrib.serializers import openapi
from fastapi_contrib.serializers.common import Serializer
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module


class BaseInventory(BaseModel):
    drugstore_id: Optional[str]


class DrugstorePrice(BaseInventory):
    drugstore_price: Optional[float] = 0


class DrugstoreBalance(BaseInventory):
    drugstore_balance: Optional[int] = 0


class Preorder(BaseInventory):
    preorder_price: Optional[float] = 0
    preorder_balance: Optional[int] = 0
    preorder_supply_date: Optional[datetime]


class Inventory(DrugstorePrice, DrugstoreBalance, Preorder):
    pass


class BaseList(BaseModel):
    id: str
    value: Optional[Union[int, float, bool]]
    list_items: Sequence[Union[DrugstoreBalance, DrugstorePrice, Preorder]]

    def __iter__(self):
        return iter(self.list_items)

    def get_msg(self):
        include = {"id", "value"}
        body = self.json(include=include, by_alias=True).encode()
        return Message(body=body)

    @classmethod
    def get_exchange(cls):
        return cls.Config.fields.get("value")


class Balancelist(BaseList):
    value: Optional[int] = 0
    list_items: List[DrugstoreBalance] = Field(alias="drugstore_balances")

    class Config:
        fields = {"value": "q_ds"}


class Pricelist(BaseList):
    value: Optional[float] = 0
    list_items: List[DrugstorePrice] = Field(alias="drugstore_prices")

    class Config:
        fields = {"value": "min_price"}


class Preorderlist(BaseList):
    value: Optional[bool] = True
    list_items: List[Preorder] = Field(alias="preorders")

    class Config:
        fields = {"value": "preorder"}


class Inventories(BaseModel):
    id: str
    inventorylist: Optional[List[Inventory]] = None


@openapi.patch
class InventoriesSerializer(Serializer):
    class Meta:
        model = Inventories


BaseListT = TypeVar("BaseListT", Balancelist, Pricelist, Preorderlist)
