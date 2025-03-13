from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
import logging
import sys
from config import APP_PORT
from shared import RabbitMQClient


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("core")


@asynccontextmanager
async def lifespan(app: FastAPI):
    RabbitMQClient().setup_queues()
    yield


app = FastAPI(title="Core Service", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Core Service is running"}


if __name__ == "__main__":
    logger.info("Starting Core")
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)