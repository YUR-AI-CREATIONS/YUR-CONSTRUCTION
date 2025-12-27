# BID-ZONE Deployment Guide

## One-Button Deployment

### Prerequisites

1. **Docker & Docker Compose**
   ```bash
   # Install Docker (Ubuntu/Debian)
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Install Docker Compose
   sudo apt-get install docker-compose
   ```

2. **Environment Configuration**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your API keys
   nano .env
   ```

### Quick Deploy

```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f bid-zone

# Stop services
docker-compose down
```

### Health Check

```bash
# Check application health
curl http://localhost:5000/health

# Expected response: {"status": "healthy", "version": "1.0.0"}
```

---

## Production Deployment

### 1. Environment Setup

**Required Environment Variables:**

```env
# AI API Keys (at least one required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
GEMINI_API_KEY=...

# Security
SECRET_KEY=<generate-secure-random-key>

# Database (for production use PostgreSQL)
DATABASE_URL=postgresql://user:pass@host:5432/bidzone

# Performance
WORKERS=4
TIMEOUT=300
```

### 2. Build & Deploy

```bash
# Build the image
docker-compose build

# Run in detached mode
docker-compose up -d

# Scale workers if needed
docker-compose up -d --scale bid-zone=3
```

### 3. Database Initialization

```bash
# Run migrations (if using PostgreSQL)
docker-compose exec bid-zone python -c "from src.database import init_db; init_db()"
```

### 4. Volume Management

The following volumes are created:
- `./uploads` - Uploaded project files
- `./outputs` - Generated estimates and reports
- `./temp` - Temporary processing files
- `./logs` - Application logs

Ensure proper permissions:
```bash
mkdir -p uploads outputs temp logs
chmod 777 uploads outputs temp logs
```

---

## Smoke Testing

### 1. System Health Check

```bash
# Check all services
docker-compose ps

# Should show:
# bid-zone-app    running    0.0.0.0:5000->5000/tcp
# bid-zone-redis  running    0.0.0.0:6379->6379/tcp
```

### 2. API Endpoint Tests

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test system status
curl http://localhost:5000/api/status

# Test file upload (example)
curl -X POST -F "file=@test_plan.pdf" \
  -F "project_name=Test Project" \
  http://localhost:5000/api/upload
```

### 3. Agent Coordination Test

```bash
# Run built-in test suite
docker-compose exec bid-zone python test_system.py

# Expected output:
# ✓ File ingestion working
# ✓ Document chunking working
# ✓ Agent framework working
# ✓ Agent coordination working (no overtalk)
# ✓ Oracle verification working
# ✓ Nucleus aggregation working
# ✓ Excel export working
# All systems operational!
```

---

## Troubleshooting

### Common Issues

**1. Container won't start**
```bash
# Check logs
docker-compose logs bid-zone

# Common causes:
# - Missing API keys in .env
# - Port 5000 already in use
# - Insufficient memory
```

**2. API key errors**
```bash
# Verify environment variables are loaded
docker-compose exec bid-zone env | grep API_KEY

# Restart after .env changes
docker-compose restart
```

**3. File upload failures**
```bash
# Check volume permissions
ls -la uploads/

# Fix permissions
sudo chmod 777 uploads outputs temp
```

**4. Out of memory errors**
```bash
# Increase Docker memory limit in Docker Desktop settings
# Or in docker-compose.yml add:
services:
  bid-zone:
    deploy:
      resources:
        limits:
          memory: 8G
```

---

## Monitoring & Logs

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f bid-zone

# Last 100 lines
docker-compose logs --tail=100 bid-zone
```

### Application Logs

```bash
# View application log file
tail -f logs/bid_zone.log

# View audit log
tail -f logs/audit.log
```

### Performance Metrics

```bash
# Container stats
docker stats bid-zone-app

# Resource usage
docker-compose top
```

---

## Scaling & Performance

### Horizontal Scaling

```bash
# Run multiple instances
docker-compose up -d --scale bid-zone=3

# Use nginx for load balancing
# (see nginx.conf.example)
```

### Performance Tuning

**Environment Variables:**
```env
# Increase workers for better throughput
WORKERS=8

# Adjust timeout for large files
TIMEOUT=600

# Enable caching
ENABLE_CACHING=True
REDIS_URL=redis://redis:6379/0

# Limit concurrent agents
MAX_PARALLEL_AGENTS=4
```

---

## Backup & Recovery

### Backup Data

```bash
# Backup uploads and outputs
tar -czf backup-$(date +%Y%m%d).tar.gz uploads/ outputs/ logs/

# Backup database
docker-compose exec postgres pg_dump -U postgres bidzone > backup.sql
```

### Restore Data

```bash
# Restore files
tar -xzf backup-20250127.tar.gz

# Restore database
docker-compose exec -T postgres psql -U postgres bidzone < backup.sql
```

---

## Security Best Practices

1. **API Keys**
   - Never commit .env to repository
   - Rotate keys regularly
   - Use separate keys for dev/prod

2. **Network Security**
   - Use HTTPS in production (reverse proxy)
   - Implement rate limiting
   - Enable firewall rules

3. **File Upload Security**
   - Validate file types
   - Scan for malware
   - Limit file sizes

4. **Container Security**
   - Run as non-root user
   - Keep images updated
   - Scan for vulnerabilities

---

## Maintenance

### Update Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

### Clean Up

```bash
# Remove old images
docker image prune -a

# Clean build cache
docker builder prune

# Remove unused volumes
docker volume prune
```

---

## Support & Documentation

- [README.md](README.md) - Overview and features
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Implementation details
- [USER_GUIDE.md](USER_GUIDE.md) - User documentation

For issues: https://github.com/YUR-AI-CREATIONS/BID-ZONE-/issues

---

## Version Information

**Current Version:** 1.0.0  
**Docker Image:** bid-zone:latest  
**Python Version:** 3.11  
**Status:** Production Ready ✅
