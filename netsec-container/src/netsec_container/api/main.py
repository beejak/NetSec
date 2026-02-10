"""FastAPI application for container security scanner"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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


@app.get("/", response_class=HTMLResponse)
async def root():
    """API root endpoint - serves web interface"""
    # Return the web interface HTML
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NetSec-Container Scanner</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }
        h1 { color: #333; margin-bottom: 10px; font-size: 2em; }
        .subtitle { color: #666; margin-bottom: 30px; }
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            background: #f8f9ff;
        }
        .upload-area:hover { border-color: #764ba2; background: #f0f2ff; }
        .upload-area.dragover { border-color: #764ba2; background: #e8ebff; transform: scale(1.02); }
        .upload-icon { font-size: 48px; margin-bottom: 20px; }
        .upload-text { color: #667ee2; font-size: 1.1em; margin-bottom: 10px; }
        .upload-hint { color: #999; font-size: 0.9em; }
        input[type="file"] { display: none; }
        .image-input { margin-top: 20px; }
        .image-input input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
        }
        .scan-button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            margin-top: 20px;
            transition: transform 0.2s;
        }
        .scan-button:hover { transform: translateY(-2px); }
        .scan-button:disabled { opacity: 0.6; cursor: not-allowed; }
        .progress { display: none; margin-top: 20px; }
        .progress.active { display: block; }
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #f0f0f0;
            border-radius: 4px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.3s;
            animation: pulse 2s infinite;
        }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
        .results { display: none; margin-top: 30px; padding: 20px; background: #f8f9ff; border-radius: 10px; }
        .results.active { display: block; }
        .result-item {
            margin-bottom: 15px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .result-label { font-weight: bold; color: #333; margin-bottom: 5px; }
        .result-value { color: #666; }
        .detail-list { margin-top: 10px; max-height: 200px; overflow-y: auto; }
        .detail-item { font-size: 0.9em; padding: 8px; background: #fff; border-radius: 6px; margin-bottom: 6px; border-left: 3px solid #667eea; }
        .detail-item.critical { border-left-color: #c33; }
        .detail-item.high { border-left-color: #e67e22; }
        .detail-item.medium { border-left-color: #f1c40f; }
        .error {
            display: none;
            margin-top: 20px;
            padding: 15px;
            background: #fee;
            border: 2px solid #fcc;
            border-radius: 8px;
            color: #c33;
        }
        .error.active { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐳 NetSec-Container</h1>
        <p class="subtitle">Lightweight Container Security Scanner</p>
        
        <div class="upload-area" id="uploadArea">
            <div class="upload-icon">📦</div>
            <div class="upload-text">Drag & Drop Image File Here</div>
            <div class="upload-hint">or click to select</div>
            <input type="file" id="fileInput" accept=".tar,.tar.gz,.tgz" />
        </div>
        
        <div class="image-input">
            <input type="text" id="imageInput" placeholder="Or enter image name (e.g., docker.io/library/nginx:latest)" />
        </div>
        
        <button class="scan-button" id="scanButton" onclick="startScan()">🔍 Scan Container</button>
        
        <div class="progress" id="progress">
            <div class="progress-bar"><div class="progress-fill"></div></div>
            <p style="text-align: center; margin-top: 10px; color: #666;">Scanning in progress...</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="results" id="results">
            <h3 style="margin-bottom: 20px;">📊 Scan Results</h3>
            <div id="resultsContent"></div>
        </div>
    </div>
    
    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const imageInput = document.getElementById('imageInput');
        const scanButton = document.getElementById('scanButton');
        const progress = document.getElementById('progress');
        const results = document.getElementById('results');
        const error = document.getElementById('error');
        const resultsContent = document.getElementById('resultsContent');
        
        uploadArea.addEventListener('click', () => fileInput.click());
        uploadArea.addEventListener('dragover', (e) => { e.preventDefault(); uploadArea.classList.add('dragover'); });
        uploadArea.addEventListener('dragleave', () => { uploadArea.classList.remove('dragover'); });
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            if (e.dataTransfer.files.length > 0) {
                fileInput.files = e.dataTransfer.files;
                updateScanButton();
            }
        });
        
        fileInput.addEventListener('change', updateScanButton);
        imageInput.addEventListener('input', updateScanButton);
        
        function updateScanButton() {
            scanButton.disabled = !fileInput.files.length && !imageInput.value.trim();
        }
        
        async function startScan() {
            const file = fileInput.files[0];
            const image = imageInput.value.trim();
            
            if (!file && !image) {
                showError('Please select a file or enter an image name');
                return;
            }
            
            error.classList.remove('active');
            results.classList.remove('active');
            progress.classList.add('active');
            scanButton.disabled = true;
            
            try {
                let response;
                
                if (file) {
                    const formData = new FormData();
                    formData.append('file', file);
                    formData.append('format', 'json');
                    
                    response = await fetch('/api/v1/scan/upload', {
                        method: 'POST',
                        body: formData
                    });
                } else {
                    response = await fetch('/api/v1/scan', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            image: image,
                            enable_vulnerability: true,
                            enable_secrets: true,
                            enable_sbom: true
                        })
                    });
                }
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Scan failed');
                }
                
                const data = await response.json();
                displayResults(data);
                
            } catch (err) {
                showError(err.message || 'An error occurred during scanning');
            } finally {
                progress.classList.remove('active');
                scanButton.disabled = false;
            }
        }
        
        function displayResults(data) {
            const results_data = data.results || data;
            const vulns = results_data.vulnerabilities || [];
            const secrets = results_data.secrets || [];
            const maxShow = 10;
            
            let html = `
                <div class="result-item">
                    <div class="result-label">Risk Score</div>
                    <div class="result-value">${results_data.risk_score ?? 0}/100 (${(results_data.risk_level || 'unknown').toUpperCase()})</div>
                </div>
                <div class="result-item">
                    <div class="result-label">Vulnerabilities</div>
                    <div class="result-value">${vulns.length} found</div>
                    ${vulns.length ? `<div class="detail-list">${vulns.slice(0, maxShow).map(v => `
                        <div class="detail-item ${(v.severity || '').toLowerCase()}">
                            ${v.cve_id || v.package || 'N/A'} ${v.severity ? '(' + v.severity + ')' : ''} ${v.description ? ': ' + (v.description.substring(0, 60) + (v.description.length > 60 ? '...' : '')) : ''}
                        </div>
                    `).join('')}${vulns.length > maxShow ? `<div class="detail-item">... and ${vulns.length - maxShow} more</div>` : ''}</div>` : ''}
                </div>
                <div class="result-item">
                    <div class="result-label">Secrets</div>
                    <div class="result-value">${secrets.length} found</div>
                    ${secrets.length ? `<div class="detail-list">${secrets.slice(0, maxShow).map(s => `
                        <div class="detail-item high">
                            ${s.type || 'Secret'} ${s.file_path ? ' in ' + s.file_path : ''}
                        </div>
                    `).join('')}${secrets.length > maxShow ? `<div class="detail-item">... and ${secrets.length - maxShow} more</div>` : ''}</div>` : ''}
                </div>
            `;
            
            resultsContent.innerHTML = html;
            results.classList.add('active');
        }
        
        function showError(message) {
            error.textContent = message;
            error.classList.add('active');
        }
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)


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
        
        return JSONResponse(content={
            "success": True,
            "results": results.to_dict(),
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/scan/upload")
async def scan_uploaded_image(
    file: UploadFile = File(...),
    enable_llm: bool = False,
    format: str = "json",
):
    """
    Scan uploaded container image file
    
    Args:
        file: Uploaded image tar file
        enable_llm: Enable LLM remediation
        format: Report format (pdf, csv, json)
        
    Returns:
        Generated report file or JSON results
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
        
        # Return JSON for web interface, or file for download
        if format == "json":
            return JSONResponse(content={
                "success": True,
                "results": results.to_dict(),
            })
        else:
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
