from fastapi import APIRouter, HTTPException
from models.customer import Customer, CustomerCreate
from routes import get_next_customer_id
from database import customers_collection, accounts_collection

from config import PREMIUM_BALANCE, NEXT_CUSTOMER_ID

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

    customers = list(customers_collection.find())

    for customer in customers:
        customer.pop("_id", None)

    matches = [
        customer
        for customer in customers
        if name.lower() in customer["name"].lower()
    ]

    if not matches:
        raise HTTPException(
            status_code=404,
            detail="No customers found with that name"
        )

    return matches

# get premium customers
@router.get("/api/customers/premium")
def get_premium_customers():

    premium = []
    customers = list(customers_collection.find())
    accounts = list(accounts_collection.find())

    for customer in customers:

        total_balance = sum(
            account.balance
            for account in accounts
            if account.customer_id == customer.id
        )

        if total_balance >= PREMIUM_BALANCE:
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

    customer.pop("id", None)

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
def update_customer(id: int, updated_customer: Customer):

    for index, customer in enumerate(customers):

        if customer.id == id:

            updated_customer.id = id

            customers[index] = updated_customer

            return updated_customer

    raise HTTPException(
        status_code=404,
        detail="Customer not found"
    )

# delete customer
@router.delete("/api/customers/{id}")
def delete_customer(id: int):

    customer = None

    for c in customers:
        if c.id == id:
            customer = c
            break

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    accounts[:] = [
        account
        for account in accounts
        if account.customer_id != id
    ]

    customers.remove(customer)

    return {
        "message": "Customer deleted"
    }

