"""Simple web interface for container scanning"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import tempfile
import asyncio

from netsec_container import ContainerScanner

# Create templates directory if it doesn't exist
templates_dir = Path(__file__).parent / "templates"
templates_dir.mkdir(exist_ok=True)

app = FastAPI(
    title="NetSec-Container Web Interface",
    description="Web interface for container security scanning",
    version="0.1.0",
)

templates = Jinja2Templates(directory=str(templates_dir))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main web interface"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NetSec-Container Scanner</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
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
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2em;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
        }
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            background: #f8f9ff;
        }
        .upload-area:hover {
            border-color: #764ba2;
            background: #f0f2ff;
        }
        .upload-area.dragover {
            border-color: #764ba2;
            background: #e8ebff;
            transform: scale(1.02);
        }
        .upload-icon {
            font-size: 48px;
            margin-bottom: 20px;
        }
        .upload-text {
            color: #667ee2;
            font-size: 1.1em;
            margin-bottom: 10px;
        }
        .upload-hint {
            color: #999;
            font-size: 0.9em;
        }
        input[type="file"] {
            display: none;
        }
        .image-input {
            margin-top: 20px;
        }
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
        .scan-button:hover {
            transform: translateY(-2px);
        }
        .scan-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .progress {
            display: none;
            margin-top: 20px;
        }
        .progress.active {
            display: block;
        }
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
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        .results {
            display: none;
            margin-top: 30px;
            padding: 20px;
            background: #f8f9ff;
            border-radius: 10px;
        }
        .results.active {
            display: block;
        }
        .result-item {
            margin-bottom: 15px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .result-label {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        .result-value {
            color: #666;
        }
        .download-button {
            display: inline-block;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            margin-top: 10px;
            margin-right: 10px;
        }
        .error {
            display: none;
            margin-top: 20px;
            padding: 15px;
            background: #fee;
            border: 2px solid #fcc;
            border-radius: 8px;
            color: #c33;
        }
        .error.active {
            display: block;
        }
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
            <div class="progress-bar">
                <div class="progress-fill"></div>
            </div>
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
        
        // Drag and drop
        uploadArea.addEventListener('click', () => fileInput.click());
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
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
            
            // Reset UI
            error.classList.remove('active');
            results.classList.remove('active');
            progress.classList.add('active');
            scanButton.disabled = true;
            
            try {
                let response;
                
                if (file) {
                    // Upload file
                    const formData = new FormData();
                    formData.append('file', file);
                    formData.append('format', 'json');
                    
                    response = await fetch('/api/v1/scan/upload', {
                        method: 'POST',
                        body: formData
                    });
                } else {
                    // Scan by image name
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
            
            let html = `
                <div class="result-item">
                    <div class="result-label">Risk Score</div>
                    <div class="result-value">${results_data.risk_score || 0}/100 (${(results_data.risk_level || 'unknown').toUpperCase()})</div>
                </div>
                <div class="result-item">
                    <div class="result-label">Vulnerabilities</div>
                    <div class="result-value">${(results_data.vulnerabilities || []).length} found</div>
                </div>
                <div class="result-item">
                    <div class="result-label">Secrets</div>
                    <div class="result-value">${(results_data.secrets || []).length} found</div>
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
