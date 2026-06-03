from fastapi import APIRouter, HTTPException
from models.account import Account, AccountCreate
from .routes import get_next_account_id
from db.database import customers_collection, accounts_collection

router = APIRouter()

# get all accounts
@router.get("/api/accounts")
def get_all_accounts():
    accounts = list(accounts_collection.find())

    for account in accounts:
        account.pop("_id", None)

    return accounts

# get account by customer name
@router.get("/api/accounts/search")
def get_accounts_by_name(name: str):

    matches = [account for account in accounts_collection.find() for customer in customers_collection.find() if account["customer_id"] == customer["id"] and name.lower() in customer["name"].lower()]
    for account in matches:
        account.pop("_id", None)

    return matches

# get account by id
@router.get("/api/accounts/{id}")
def get_account_by_id(id: int):

    account = accounts_collection.find_one({"id": id})
    
    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    account.pop("_id", None)

    return account

# create account
@router.post("/api/accounts", status_code=201)
def create_account(account_data: AccountCreate):
    
    account = Account(
        id=get_next_account_id(),
        account_number=account_data.account_number,
        account_type=account_data.account_type,
        balance=account_data.balance,
        customer_id=account_data.customer_id
    )

    account_dict = account.model_dump()

    accounts_collection.insert_one(account_dict)

    return account

# update account
@router.put("/api/accounts/{id}")
def update_account(id: int, updated_account: AccountCreate):

    result = accounts_collection.update_one(
        {"id": id},
        {"$set": updated_account.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return updated_account

# delete account
@router.delete("/api/accounts/{id}")
def delete_account(id: int):

    result = accounts_collection.delete_one({"id": id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return {"message": "Account deleted"}