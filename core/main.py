from fastapi import FastAPI
import uvicorn

from config import APP_PORT

app = FastAPI(title="Core Service")

@app.get("/")
async def root():
    return {"message": "Core Service is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)