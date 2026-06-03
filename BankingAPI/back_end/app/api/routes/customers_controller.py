from fastapi import APIRouter, HTTPException
from models.customer import Customer, CustomerCreate
from .routes import get_next_customer_id
from db.database import customers_collection, accounts_collection

from core.config import PREMIUM_BALANCE

router = APIRouter()

# get all customers
@router.get("/api/customers")
def get_all_customers():

    customers = list(customers_collection.find())

    for customer in customers:
        customer.pop("_id", None)

    return customers

# get customers by name
@router.get("/api/customers/search")
def get_customer_by_name(name: str):

    matches = [customer for customer in customers_collection.find() if name.lower() in customer["name"].lower()]
    for customer in matches:
        customer.pop("_id", None)

    return matches

# get premium customers
@router.get("/api/customers/premium")
def get_premium_customers():

    premium = []
    
    customers = list(customers_collection.find())
    accounts = list(accounts_collection.find())

    for customer in customers:

        total_balance = sum(
            account["balance"]
            for account in accounts
            if account["customer_id"] == customer["id"]
        )

        if total_balance >= PREMIUM_BALANCE:
            customer.pop("_id", None)
            premium.append(customer)

    return premium

# get customers by id
@router.get("/api/customers/{id}")
def get_customer_by_id(id: int):
    customer = customers_collection.find_one({"id": id})

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.pop("_id", None)

    return customer

# create customer
@router.post("/api/customers", response_model=Customer)
def create_customer(customer_data: CustomerCreate):

    customer = Customer(
        id=get_next_customer_id(),
        name=customer_data.name,
        email=customer_data.email,
    )

    customer_dict = customer.model_dump()

    customers_collection.insert_one(customer_dict)

    return customer

# update customer
@router.put("/api/customers/{id}")
def update_customer(id: int, updated_customer: CustomerCreate):

    result = customers_collection.update_one(
        {"id": id},
        {"$set": updated_customer.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return updated_customer

# delete customer
@router.delete("/api/customers/{id}")
def delete_customer(id: int):

    result = customers_collection.delete_one({"id": id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    accounts_collection.delete_many({"customer_id": id})

    return {"message": "Customer deleted"}

