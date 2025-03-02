from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from config import APP_PORT
from init_rabbitmq import setup_queues


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_queues()
    yield


app = FastAPI(title="Core Service", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Core Service is running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)