from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging
import random
import asyncio
from otel_config import setup_otel

setup_otel("database")
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/store")
async def store_data():
    logger.info("Database: storing data")
    try:
        await asyncio.sleep(random.uniform(0.1, 0.3))  # Асинхронная задержка

        if random.random() < 0.1:
            logger.error("Database timeout", extra={"error.type": "timeout"})
            raise TimeoutError("Database operation timed out")

        logger.info("Database: data stored successfully")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Database error: {e}")
        return JSONResponse(content={"status": "error"}, status_code=500)