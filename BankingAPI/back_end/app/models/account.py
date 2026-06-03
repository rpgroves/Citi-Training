from pydantic import BaseModel

class AccountCreate(BaseModel):
    account_number: str
    account_type: str
    balance: float
    customer_id: int

class Account(AccountCreate):
    id: int