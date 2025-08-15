from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
import logging
from otel_config import setup_otel

# Настраиваем OpenTelemetry
setup_otel("gateway")
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/process")
async def process_request():
    logger.info("Gateway: received request")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get("http://processor:8001/process")
            resp.raise_for_status()
        logger.info("Gateway: request processed successfully")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Gateway error: {e}")
        return JSONResponse(content={"status": "error"}, status_code=500)