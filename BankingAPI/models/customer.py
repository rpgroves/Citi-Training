from pydantic import BaseModel
from typing import List
from .account import Account

class Customer(BaseModel):
    id: int
    name: str
    email: str
    accounts: List[int] = []