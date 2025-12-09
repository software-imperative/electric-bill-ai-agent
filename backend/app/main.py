from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import init_db
from app.routes import (
    bills_router,
    calls_router,
    payments_router,
    vapi_webhooks_router
)
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Adani Bill Collection AI Agent",
    description="AI-powered voice agent for automated bill collection with SMS payment links",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and perform startup tasks"""
    logger.info("Starting up application...")
    init_db()
    logger.info("Database initialized successfully")


# Include routers
app.include_router(bills_router)
app.include_router(calls_router)
app.include_router(payments_router)
app.include_router(vapi_webhooks_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Adani Bill Collection AI Agent API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "bill-collection-ai-agent"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
