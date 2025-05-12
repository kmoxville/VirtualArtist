from contextlib import contextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
import sys
from config import APP_PORT
from shared import RabbitMQClient
from storage import StorageService
from api.v1.prompt import router as prompts_router
from api.v1.messages import router as messages_router
from api.v1.audio import router as audio_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("core")
storage_service = StorageService()


def lifespan(app: FastAPI):
    RabbitMQClient().setup_queues()
    storage_service.start_consumers()

    yield
    
    storage_service.stop_consumers()


app = FastAPI(title="Core Service", lifespan=lifespan)
app.include_router(prompts_router, prefix="/api/v1/prompt")
app.include_router(messages_router, prefix="/api/v1/messages")
app.include_router(audio_router, prefix="/api/v1/audio")

origins = [
    "http://localhost:5173",  # Vite dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Разрешённые источники
    allow_credentials=True,
    allow_methods=["*"],               # Разрешить все методы (GET, POST и т.д.)
    allow_headers=["*"],               # Разрешить все заголовки
)

@app.get("/")
def root():
    return {"message": "Core Service is running"}


if __name__ == "__main__":
    logger.info("Starting Core")
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)