# NetSec-Core Deployment Guide

This guide covers various deployment options for NetSec-Core.

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run API server
python run_api.py
# or
uvicorn netsec_core.api.main:app --reload
```

## Docker Deployment

### Build Docker Image

```bash
docker build -t netsec-core:latest .
```

### Run with Docker

```bash
docker run -d \
  --name netsec-core \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your-key-here \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/data:/app/data \
  netsec-core:latest
```

### Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=false
API_WORKERS=4

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/netsec-core.log

# Scanner Settings
SCAN_TIMEOUT=5.0
SCAN_MAX_WORKERS=50
DNS_TIMEOUT=5.0

# SSL/TLS
SSL_TIMEOUT=10.0
SSL_CHECK_EXPIRATION_DAYS=30

# LLM (Optional)
LLM_PROVIDER=openai
LLM_MODEL=gpt-3.5-turbo
OPENAI_API_KEY=your-key-here
# or
ANTHROPIC_API_KEY=your-key-here

# Anomaly Detection
ANOMALY_THRESHOLD=3.0
ANOMALY_LEARNING_DURATION=3600

# Traffic Analysis
TRAFFIC_CAPTURE_TIMEOUT=60
TRAFFIC_MAX_PACKETS=10000

# CORS
CORS_ORIGINS=*
CORS_CREDENTIALS=true
```

## Production Deployment

### Systemd Service

Create `/etc/systemd/system/netsec-core.service`:

```ini
[Unit]
Description=NetSec-Core API Service
After=network.target

[Service]
Type=simple
User=netsec
WorkingDirectory=/opt/netsec-core
Environment="PATH=/opt/netsec-core/venv/bin"
ExecStart=/opt/netsec-core/venv/bin/uvicorn netsec_core.api.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable netsec-core
sudo systemctl start netsec-core
sudo systemctl status netsec-core
```

### Nginx Reverse Proxy

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name netsec-core.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL/TLS with Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d netsec-core.example.com
```

## Kubernetes Deployment

### Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: netsec-core
spec:
  replicas: 3
  selector:
    matchLabels:
      app: netsec-core
  template:
    metadata:
      labels:
        app: netsec-core
    spec:
      containers:
      - name: netsec-core
        image: netsec-core:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: netsec-secrets
              key: openai-api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: netsec-core-service
spec:
  selector:
    app: netsec-core
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

## Security Considerations

### Network Security

- Use firewall rules to restrict access
- Implement rate limiting
- Use HTTPS/TLS for production
- Restrict CORS origins

### Authentication (Future Enhancement)

- Implement API key authentication
- Add OAuth2/JWT support
- Role-based access control

### Resource Limits

- Set appropriate memory and CPU limits
- Implement request timeouts
- Monitor resource usage

## Monitoring

### Health Checks

```bash
# Health endpoint
curl http://localhost:8000/api/v1/health

# Docker health check
docker inspect --format='{{.State.Health.Status}}' netsec-core
```

### Logging

Logs are written to:
- Console (stdout)
- File: `logs/netsec-core.log` (configurable)

### Metrics (Future Enhancement)

- Prometheus metrics endpoint
- Grafana dashboards
- Alerting rules

## Backup and Recovery

### Data Backup

```bash
# Backup data directory
tar -czf netsec-core-backup-$(date +%Y%m%d).tar.gz data/ logs/
```

### Configuration Backup

```bash
# Backup configuration
cp .env .env.backup
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill process or change port
   ```

2. **Permission denied (traffic capture)**
   ```bash
   # On Linux, may need capabilities
   sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/python3
   ```

3. **LLM not working**
   - Check API keys are set
   - Verify network connectivity
   - Check API quotas

4. **High memory usage**
   - Reduce scan_max_workers
   - Limit traffic capture size
   - Implement result pagination

## Scaling

### Horizontal Scaling

- Run multiple API instances
- Use load balancer (Nginx, HAProxy)
- Share state via Redis (future)

### Vertical Scaling

- Increase workers: `--workers 4`
- Increase memory limits
- Optimize database queries (future)

## Updates

### Updating NetSec-Core

```bash
# Pull latest code
git pull

# Rebuild Docker image
docker build -t netsec-core:latest .

# Restart services
docker-compose restart
# or
sudo systemctl restart netsec-core
```

## Support

For issues and questions:
- Check logs: `logs/netsec-core.log`
- Review documentation
- Check GitHub issues
- Contact support team
