from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import uvicorn
from pathlib import Path

from app.core.config import settings
from app.api.routers import stock
from app.services.stock_data import StockDataService

# Configure logging
logger.add(
    settings.LOG_FILE,
    rotation="1 day",
    retention="7 days",
    level=settings.LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(stock.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return JSONResponse(
        content={
            "message": "Welcome to Stock Platform API",
            "version": "1.0.0",
            "docs_url": "/docs",
            "redoc_url": "/redoc"
        }
    )

@app.get("/health")
async def health_check():
    # Check cache directory
    try:
        cache_dir = Path(settings.CACHE_DIR)
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)
        cache_status = "healthy"
    except Exception as e:
        cache_status = f"unhealthy: {str(e)}"

    return JSONResponse(
        content={
            "status": "healthy",
            "version": "1.0.0",
            "database_status": "not configured",
            "cache_status": cache_status
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 