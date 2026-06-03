from fastapi import APIRouter
from db.database import customers_collection, accounts_collection
from db.database import counters_collection

router = APIRouter()

@router.post("/customers")
async def create_customer_2():

    customer = {
        "customer_id": 1,
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com"
    }

    result = customers_collection.insert_one(customer)

    return {
        "message": "Customer created",
        "id": str(result.inserted_id)
    }

@router.post("/accounts")
async def create_account_2():

    account = {
        "account_id": 1001,
        "customer_id": 1,
        "account_type": "checking",
        "balance": 1000.00
    }

    result = accounts_collection.insert_one(account)

    return {
        "message": "Account created",
        "id": str(result.inserted_id)
    }

@router.post("/counter")
async def create_counters():

    customer_counter = {
    "_id": "customer_id",
    "value": 100001
    }

    account_counter = {
    "_id": "account_id",
    "value": 1001
    }

    result1 = counters_collection.insert_one(customer_counter)
    result2 = counters_collection.insert_one(account_counter)

    return {
        "message": "Counters created",
        "id": str(result1.inserted_id + result2.inserted_id)
    }

from pymongo import ReturnDocument

def get_next_customer_id():
    counter = counters_collection.find_one_and_update(
        {"_id": "customer_id"},
        {"$inc": {"value": 1}},
        return_document=ReturnDocument.AFTER
    )

    return counter["value"]

def get_next_account_id():
    counter = counters_collection.find_one_and_update(
        {"_id": "account_id"},
        {"$inc": {"value": 1}},
        return_document=ReturnDocument.AFTER
    )

    return counter["value"]