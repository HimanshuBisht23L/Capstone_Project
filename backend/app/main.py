from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time
from app.core.config import settings
from app.core.database import engine, Base
import app.models # Register all ORM models
from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI Lifespan context manager for application startup and shutdown events.
    Automatically initializes PostgreSQL tables on boot.
    """
    print("🚀 SheetPilot AI Backend Gateway initializing...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ PostgreSQL Database tables initialized successfully.")
    except Exception as e:
        print(f"⚠️ PostgreSQL Database connection warning: {e}")
    yield
    print("🛑 SheetPilot AI Backend Gateway shutting down...")

app = FastAPI(
    title="SheetPilot AI Engine API",
    description="Natural Language AI Spreadsheet Automation Platform Powered by FastAPI, PostgreSQL, Redis, and AST Security Sandboxing.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration allowing requests from Next.js Frontend and Streamlit Control Room
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "SheetPilot AI Backend Engine",
        "version": "1.0.0",
        "docs_url": "/docs",
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "database": "postgresql+asyncpg",
        "redis": "redis://localhost:6379",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
