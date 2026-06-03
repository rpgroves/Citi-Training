from fastapi import FastAPI
from fastapi import HTTPException
from datastore import customers, accounts
from models.customer import Customer
from models.account import Account
from seeddata import seed_data
from contextlib import asynccontextmanager
from controllers import customers_controller, accounts_controller
from routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_data()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(customers_controller.router)
app.include_router(accounts_controller.router)
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Banking API is running"}


from database import customers_collection

@app.get("/test-db")
def test_db():

    customers_collection.insert_one({
        "test": "connected"
    })

    return {"message": "MongoDB connected"}