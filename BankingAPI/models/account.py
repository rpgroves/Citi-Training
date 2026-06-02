from pydantic import BaseModel

class Account(BaseModel):
    id: int
    account_number: str
    account_type: str
    balance: float
    customer_id: int