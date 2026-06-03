from pydantic import BaseModel

class CustomerCreate(BaseModel):
    name: str
    email: str

class Customer(CustomerCreate):
    id: int
    
