from fastapi import FastAPI
from fastapi import HTTPException
from contextlib import asynccontextmanager
from api.routes import customers_controller, accounts_controller, routes
from db.database import customers_collection
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customers_controller.router)
app.include_router(accounts_controller.router)
app.include_router(routes.router)

@app.get("/")
def root():
    return {"message": "Banking API is running"}

@app.get("/test-db-connection")
def test_db():

    customers_collection.insert_one({
        "test": "connected"
    })

    return {"message": "MongoDB connected"}