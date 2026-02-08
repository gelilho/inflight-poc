"""FastAPI Application Entry Point"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.services.destination_service import destination_service
from config.constants import PREWARM_AIRPORTS, PREWARM_LANGUAGES
import logging
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle.

    On startup: pre-warm the destination cache in a background thread
    so the API keeps accepting requests while Gemini generates content.
    """
    logger.info("🚀 API starting — launching cache pre-warm in background...")

    thread = threading.Thread(
        target=destination_service.prewarm,
        args=(PREWARM_AIRPORTS, PREWARM_LANGUAGES),
        daemon=True,
    )
    thread.start()

    yield  # App is running

    logger.info("👋 API shutting down")


# Create FastAPI app
app = FastAPI(
    title="Inflight Experience API",
    description="PoC for MWC - Destination-driven inflight content system",
    version="1.0.0",
    lifespan=lifespan,
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
