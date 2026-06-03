from fastapi import APIRouter, HTTPException
from datastore import accounts, customers
from models.account import Account, AccountCreate
from routes import get_next_account_id
from database import customers_collection, accounts_collection

from config import NEXT_ACCOUNT_ID

router = APIRouter()

# get all accounts
@router.get("/api/accounts")
def get_all_accounts():
    accounts = list(accounts_collection.find())

    for account in accounts:
        account.pop("_id", None)

    return accounts

# get account by id
@router.get("/api/accounts/{id}")
def get_account_by_id(id: int):

    for account in accounts:
        if account.id == id:
            return account

    raise HTTPException(
        status_code=404,
        detail="Account not found"
    )

# get account by customer name
@router.get("/api/accounts/search")
def get_accounts_by_name(name: str):

    matching_customer_ids = []

    for customer in customers:
        if name.lower() in customer.name.lower():
            matching_customer_ids.append(customer.id)

    return [
        account
        for account in accounts
        if account.customer_id in matching_customer_ids
    ]

# create account
@router.post("/api/accounts", status_code=201)
def create_account(account_data: AccountCreate):
    
    account = Account(
        id=get_next_account_id(),
        account_number=account_data.account_number,
        account_type=account_data.account_type,
        balance=account_data.balance
    )

    account_dict = account.model_dump()

    accounts_collection.insert_one(account_dict)

    customers_collection.update_one(
        {"id": account_data.customer_id},
        {"$push": {"accounts": account.id}}
    )

    return account

# update account
@router.put("/api/accounts/{id}")
def update_account(id: int, updated_account: Account):

    for index, account in enumerate(accounts):

        if account.id == id:

            updated_account.id = id

            accounts[index] = updated_account

            return updated_account

    raise HTTPException(
        status_code=404,
        detail="Account not found"
    )

# delete account
@router.delete("/api/accounts/{id}")
def delete_account(id: int):

    account = None

    for a in accounts:
        if a.id == id:
            account = a
            break

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    accounts.remove(account)

    for customer in customers:

        customer.accounts = [
            account_id
            for account_id in customer.accounts
            if account_id != id
        ]

    return {
        "message": "Account deleted"
    }