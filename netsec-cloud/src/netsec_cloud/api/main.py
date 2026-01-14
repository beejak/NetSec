"""FastAPI application for NetSec-Cloud."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from netsec_cloud import __version__
from netsec_cloud.api.routes import scan, compliance

app = FastAPI(
    title="NetSec-Cloud API",
    version=__version__,
    description="Cloud Security Scanner API - Multi-cloud security scanning",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(scan.router, prefix="/api/v1/cloud", tags=["Cloud Scanner"])
app.include_router(compliance.router, prefix="/api/v1/cloud/compliance", tags=["Compliance"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "NetSec-Cloud API",
        "version": __version__,
        "status": "running",
        "docs": "/api/docs",
        "providers": ["aws", "azure", "gcp"],
    }


@app.get("/api/v1/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": __version__,
    }
