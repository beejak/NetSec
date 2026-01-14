"""FastAPI application for NetSec-Core."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from netsec_core.api.routes import health, dns, ssl, scan, traffic, anomaly, assets, llm, remediation
from netsec_core import __version__
from netsec_core.config import config
from netsec_core.utils.logger import logger

app = FastAPI(
    title="NetSec-Core API",
    version=__version__,
    description="Network Security Foundation Toolkit API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=config.cors_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log startup
logger.info(f"NetSec-Core API starting on {config.api_host}:{config.api_port}")
logger.info(f"API Documentation: http://{config.api_host}:{config.api_port}/api/docs")

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(dns.router, prefix="/api/v1/dns", tags=["DNS Security"])
app.include_router(ssl.router, prefix="/api/v1/ssl", tags=["SSL/TLS"])
app.include_router(scan.router, prefix="/api/v1/scan", tags=["Network Scanner"])
app.include_router(traffic.router, prefix="/api/v1/traffic", tags=["Traffic Analysis"])
app.include_router(anomaly.router, prefix="/api/v1/anomaly", tags=["Anomaly Detection"])
app.include_router(assets.router, prefix="/api/v1/assets", tags=["Asset Discovery"])
app.include_router(llm.router, prefix="/api/v1/llm", tags=["LLM Analysis"])
app.include_router(remediation.router, prefix="/api/v1/remediation", tags=["Remediation"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "NetSec-Core API",
        "version": __version__,
        "status": "running",
        "docs": "/api/docs",
    }
