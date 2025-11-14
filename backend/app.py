"""Main entrypoint for Freshness Tracker backend API.

Run this file to start the FastAPI server with Uvicorn:

    python app.py

The API will be available at http://localhost:8000
API docs: http://localhost:8000/docs
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database import engine, Base
from api.routers import batches

# Load environment variables from .env file
load_dotenv()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    api_title = os.getenv("API_TITLE", "Freshness Tracker API")
    api_version = os.getenv("API_VERSION", "1.0.0")
    cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")

    app = FastAPI(title=api_title, version=api_version)

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(batches.router)

    # Create database tables
    Base.metadata.create_all(bind=engine)

    return app


app = create_app()


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "True").lower() == "true"

    uvicorn.run("app:app", host=host, port=port, reload=reload)
