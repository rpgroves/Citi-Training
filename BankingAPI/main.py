from fastapi import FastAPI
from fastapi import HTTPException
from datastore import customers, accounts
from models.customer import Customer
from models.account import Account
from seeddata import seed_data
from contextlib import asynccontextmanager
from controllers import customers_controller, accounts_controller

@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_data()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(customers_controller.router)
app.include_router(accounts_controller.router)

@app.get("/")
def root():
    return {"message": "Banking API is running"}
