from fastapi import APIRouter, HTTPException
from datastore import customers, accounts
from models.customer import Customer

from config import PREMIUM_BALANCE, NEXT_CUSTOMER_ID

router = APIRouter()

# get all customers
@router.get("/api/customers")
def get_all_customers():
    return customers

# get customers by name
@router.get("/api/customers/search")
def get_customer_by_name(name: str):

    matches = [
        customer
        for customer in customers
        if name.lower() in customer.name.lower()
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

    for customer in customers:

        total_balance = sum(
            account.balance
            for account in customer.accounts
        )

        if total_balance >= PREMIUM_BALANCE:
            premium.append(customer)

    return premium

# get customers by id
@router.get("/api/customers/{id}")
def get_customer_by_id(id: int):
    for customer in customers:
        if customer.id == id:
            return customer

    raise HTTPException(
        status_code=404,
        detail="Customer not found"
    )

# create customer
@router.post("/api/customers", status_code=201)
def create_customer(customer: Customer):

    customer.id = NEXT_CUSTOMER_ID["value"]
    NEXT_CUSTOMER_ID["value"] += 1

    customers.append(customer)

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

