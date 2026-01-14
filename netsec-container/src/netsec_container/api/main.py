"""FastAPI application for container security scanner"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import tempfile
from pathlib import Path

from netsec_container import ContainerScanner
from netsec_container.api.models import ScanRequest, ScanResponse

app = FastAPI(
    title="NetSec-Container API",
    description="Lightweight Container Security Scanner API",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "NetSec-Container API",
        "version": "0.1.0",
        "status": "running",
    }


@app.post("/api/v1/scan", response_model=ScanResponse)
async def scan_image(request: ScanRequest):
    """
    Scan container image
    
    Args:
        request: Scan request with image name and options
        
    Returns:
        ScanResponse with results
    """
    scanner = ContainerScanner(
        enable_vulnerability=request.enable_vulnerability,
        enable_secrets=request.enable_secrets,
        enable_sbom=request.enable_sbom,
        enable_llm=request.enable_llm,
        llm_provider=request.llm_provider,
        llm_model=request.llm_model,
    )
    
    try:
        results = scanner.scan_image(
            image=request.image,
            image_file=request.image_file,
            dockerfile_path=request.dockerfile_path,
        )
        
        return ScanResponse(
            success=True,
            results=results.to_dict(),
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/scan/upload")
async def scan_uploaded_image(
    file: UploadFile = File(...),
    enable_llm: bool = False,
    format: str = "pdf",
):
    """
    Scan uploaded container image file
    
    Args:
        file: Uploaded image tar file
        enable_llm: Enable LLM remediation
        format: Report format (pdf, csv, json)
        
    Returns:
        Generated report file
    """
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tar") as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        scanner = ContainerScanner(enable_llm=enable_llm)
        
        # Scan image
        results = scanner.scan_image(
            image=file.filename,
            image_file=tmp_file_path,
        )
        
        # Generate report
        report_path = scanner.generate_report(results, format=format)
        
        # Return report file
        return FileResponse(
            report_path,
            media_type="application/pdf" if format == "pdf" else "text/csv",
            filename=f"security_report.{format}",
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Cleanup
        Path(tmp_file_path).unlink(missing_ok=True)


@app.get("/api/v1/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}
