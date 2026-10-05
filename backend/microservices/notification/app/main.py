"""Notification microservice - entry point.

Run:
    uvicorn app.main:app --reload --port 8084

or:
    python -m app.main
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

import py_eureka_client.eureka_client as eureka_client

from app.routers import notification


# ============================================================
# Configuration
# ============================================================

PORT = int(os.getenv("PORT", "8084"))

EUREKA_SERVER = os.getenv(
    "EUREKA_SERVER",
    "http://localhost:8761/eureka"
)


# ============================================================
# Eureka - Startup / Shutdown
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("======================================")
    print("Starting NOTIFICATION Microservice...")
    print(f"Port: {PORT}")
    print(f"Eureka: {EUREKA_SERVER}")
    print("======================================")

    try:
        # Enregistrement dans Eureka
        await eureka_client.init_async(
            eureka_server=EUREKA_SERVER,
            app_name="NOTIFICATION",
            instance_port=PORT,
            instance_host="localhost",
            instance_ip="localhost"
        )

        print("NOTIFICATION registered in Eureka")
        print(f"URL: http://localhost:{PORT}")

    except Exception as e:
        print("ERROR: Could not register NOTIFICATION in Eureka")
        print(e)

    # L'application continue
    yield

    # Désenregistrement à l'arrêt
    print("Stopping NOTIFICATION...")

    try:
        await eureka_client.stop_async()
        print("NOTIFICATION unregistered from Eureka")

    except Exception as e:
        print("Error while stopping Eureka client:")
        print(e)


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; "
        "the notification logic is to be developed by students."
    ),
    contact={
        "name": "Badia Abouhdid"
    },

    servers=[
        {
            "url": f"http://localhost:{PORT}",
            "description": "Local"
        }
    ],

    # Swagger UI
    docs_url="/swagger-ui",

    # OpenAPI JSON
    openapi_url="/v3/api-docs",

    # ReDoc
    redoc_url="/redoc",

    # Eureka lifecycle
    lifespan=lifespan
)


# ============================================================
# Routers
# ============================================================

app.include_router(notification.router)


# ============================================================
# Info Endpoint
# ============================================================

@app.get("/info")
async def info():
    return {
        "service": "NOTIFICATION",
        "status": "UP",
        "port": PORT
    }


# ============================================================
# Health Endpoint
# ============================================================

@app.get("/health")
async def health():
    return {
        "status": "UP",
        "service": "NOTIFICATION"
    }


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True
    )