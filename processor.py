from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
import logging
import random
from otel_config import setup_otel

setup_otel("processor")
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/process")
async def process_data():
    logger.info("Processor: start processing")
    try:
        # Имитация случайной ошибки
        if random.random() < 0.3:
            logger.error("Processor failed", extra={"error.type": "random_failure"})
            raise ValueError("Random failure")

        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get("http://database:8002/store")
            resp.raise_for_status()

        logger.info("Processor: data processed successfully")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Processor error: {e}")
        return JSONResponse(content={"status": "error"}, status_code=500)