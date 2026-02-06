"""FastAPI Application Entry Point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI app
app = FastAPI(
    title="Inflight Experience API",
    description="PoC for MWC - Destination-driven inflight content system",
    version="1.0.0"
)

# CORS middleware (for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "service": "Inflight Experience PoC",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "flow_b": "/api/v1/passenger-context/{user_id}",
            "flow_a": "/api/v1/destination-experience/{airport_code}",
            "big_flow": "/api/v1/inflight-experience/{user_id}"
        }
    }
