"""Configuration endpoints used by the frontend at runtime.

Exposes the public URL that phones should open for batch views. This avoids
hardcoding LAN IPs in the frontend build and supports dynamic discovery on
Windows/WSL.
"""

import os
from fastapi import APIRouter

router = APIRouter(prefix="/config", tags=["config"])


@router.get("/public")
def get_public_urls():
    """Return public URLs for frontend and backend.

    - public_url: base URL users/phones should open for the React app.
    - api_url: base URL for the backend (useful for diagnostics/Future use).
    """
    # Prefer dynamically set PUBLIC_HOST; else HOST; else localhost
    public_host = os.environ.get("PUBLIC_HOST") or os.environ.get("HOST") or "localhost"
    api_host = os.environ.get("HOST") or "0.0.0.0"

    frontend_port = int(os.environ.get("FRONTEND_PORT", "3000"))
    api_port = int(os.environ.get("PORT", "8000"))

    public_url = f"http://{public_host}:{frontend_port}"
    api_url = f"http://{public_host if public_host != '0.0.0.0' else 'localhost'}:{api_port}"

    return {
        "public_host": public_host,
        "public_port": frontend_port,
        "public_url": public_url,
        "api_host": api_host,
        "api_port": api_port,
        "api_url": api_url,
    }
