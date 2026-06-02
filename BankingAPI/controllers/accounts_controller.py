from fastapi import APIRouter, HTTPException
from datastore import accounts, customers
from models.account import Account

from config import NEXT_ACCOUNT_ID

router = APIRouter()

# get all accounts
@router.get("/api/accounts")
def get_all_accounts():
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
def create_account(account: Account):

    customer = None

    for c in customers:
        if c.id == account.customer_id:
            customer = c
            break

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    new_id = NEXT_ACCOUNT_ID
    NEXT_ACCOUNT_ID += 1

    account.id = new_id

    accounts.append(account)

    customer.accounts.append(account)

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
            a
            for a in customer.accounts
            if a.id != id
        ]

    return {
        "message": "Account deleted"
    }