# Quick Deployment Checklist

Use this checklist when deploying BID-ZONE to ensure all steps are covered.

## Pre-Deployment ☑️

- [ ] Review [DEPLOYMENT_READINESS.md](DEPLOYMENT_READINESS.md) report
- [ ] Ensure server meets system requirements:
  - [ ] Python 3.9+ (or Docker installed)
  - [ ] 8GB RAM recommended
  - [ ] 500MB+ disk space
  - [ ] Network access to AI service APIs

## Configuration ☑️

- [ ] Copy environment template: `cp .env.example .env`
- [ ] Add required API keys to .env:
  - [ ] OPENAI_API_KEY (minimum requirement)
  - [ ] ANTHROPIC_API_KEY (optional)
  - [ ] GOOGLE_API_KEY (optional)
  - [ ] GEMINI_API_KEY (optional)
- [ ] Set SECRET_KEY to secure random value
- [ ] Configure other settings as needed

## Choose Deployment Method ☑️

### Option A: Docker Compose (Recommended)
- [ ] Verify Docker and Docker Compose installed
- [ ] Review docker-compose.yml
- [ ] Create required directories (Docker will create them)
- [ ] Run: `docker-compose up -d`
- [ ] Check status: `docker-compose ps`

### Option B: Direct Python
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate venv: `source venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Install package: `pip install -e .`
- [ ] Create directories: `mkdir -p uploads outputs temp logs`
- [ ] Run API server: `python api_server.py`

## Post-Deployment Validation ☑️

- [ ] Wait 30 seconds for services to start
- [ ] Health check passes: `curl http://localhost:5000/health`
  - [ ] Expected response: `{"status": "healthy", "version": "1.0.0"}`
- [ ] System status check: `curl http://localhost:5000/api/status`
- [ ] View logs:
  - Docker: `docker-compose logs -f bid-zone`
  - Direct: Check `logs/bid_zone.log`

## Smoke Testing ☑️

- [ ] Run system tests: `python test_system.py`
  - [ ] All tests pass ✓
- [ ] Test file upload (if you have sample file):
  ```bash
  curl -X POST -F "file=@sample.pdf" \
       -F "project_name=Test" \
       http://localhost:5000/api/upload
  ```

## Monitoring Setup ☑️

- [ ] Verify health checks working
- [ ] Set up log rotation (for production)
- [ ] Configure backup for uploads/outputs
- [ ] Set up monitoring/alerts (optional)

## Security Checklist ☑️

- [ ] .env file has restricted permissions (600)
- [ ] API keys are not exposed in logs
- [ ] Firewall configured (if applicable)
- [ ] Rate limiting enabled (for production)
- [ ] HTTPS configured (for production)

## Documentation Review ☑️

- [ ] Team has access to [README.md](README.md)
- [ ] Team has access to [DEPLOYMENT.md](DEPLOYMENT.md)
- [ ] Team has access to [USER_GUIDE.md](USER_GUIDE.md)
- [ ] Troubleshooting guide reviewed

## Common Issues - Quick Fixes 🔧

### Container won't start
```bash
# Check logs
docker-compose logs bid-zone

# Common fix: Restart
docker-compose restart
```

### API key errors
```bash
# Verify env vars loaded
docker-compose exec bid-zone env | grep API_KEY

# Fix: Restart after .env changes
docker-compose down && docker-compose up -d
```

### Permission errors
```bash
# Fix permissions
chmod -R 777 uploads outputs temp logs
```

### Port already in use
```bash
# Edit docker-compose.yml to use different port
# Change "5000:5000" to "8080:5000"
```

## Rollback Plan ☑️

If deployment fails:
- [ ] Docker: `docker-compose down`
- [ ] Direct: Stop process (Ctrl+C or kill PID)
- [ ] Review logs for errors
- [ ] Fix issues and retry
- [ ] Restore from backup if needed

## Production Considerations ☑️

For production deployments, also consider:
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure Redis for caching
- [ ] Set up reverse proxy (nginx/Apache)
- [ ] Enable SSL/TLS certificates
- [ ] Set up automated backups
- [ ] Configure log aggregation
- [ ] Set up monitoring and alerting
- [ ] Document disaster recovery plan

## Deployment Complete! 🎉

- [ ] All checks passed
- [ ] Service is running
- [ ] Team notified
- [ ] Documentation updated with any changes

---

**Quick Reference Links:**
- Health: http://localhost:5000/health
- Status: http://localhost:5000/api/status
- Logs (Docker): `docker-compose logs -f`
- Stop (Docker): `docker-compose down`
- Restart (Docker): `docker-compose restart`

**Support:** See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed troubleshooting
