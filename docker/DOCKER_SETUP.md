# Docker Setup Guide for Log Investigator

This guide will help you containerize and deploy the Log Investigator project using Docker and Docker Compose.

## Prerequisites

- Docker installed on your system
- Docker Compose installed
- Google Gemini API key (for AI analysis)

## Quick Start

### 1. Set up Environment Variables

Create a `.env` file in the root directory:

```bash
# Copy the example environment file
cp env.example .env
```

Edit `.env` and add your Google Gemini API key:

```bash
# Required: Google Gemini API Key
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Optional: Customize other settings
GEMINI_MODEL=gemini-2.5-pro
GEMINI_MAX_TOKENS=2048
GEMINI_TEMPERATURE=0.3
```

### 2. Build and Run with Docker Compose

```bash
# Build and start all services
cd docker
./docker-helper.sh start

# Or run in detached mode
cd docker
docker-compose up --build -d
```

### 3. Access the Application

- **Frontend**: http://localhost:4000
- **Backend API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

## Docker Architecture

The project uses a multi-container setup:

### Services

1. **Backend** (`log-investigator-backend`)
   - Python Flask application
   - Port: 8000
   - Handles log analysis and AI processing
   - Dockerfile: `docker/backend.Dockerfile`

2. **Frontend** (`log-investigator-frontend`)
   - Next.js React application
   - Port: 4000
   - Web interface for uploading and viewing logs
   - Dockerfile: `docker/frontend.Dockerfile`

### Compose Files

- Development: `docker/docker-compose.yml`
- Production:  `docker/docker-compose.prod.yml`

### Volumes

- `../data` → `/app/data` (log data storage)
- `../uploads` → `/app/uploads` (uploaded files)
- `../logs` → `/app/logs` (application logs)

## Docker Commands

### Development

```bash
cd docker
./docker-helper.sh start
./docker-helper.sh logs
./docker-helper.sh status
./docker-helper.sh stop
```

### Production

```bash
cd docker
docker-compose -f docker-compose.prod.yml up --build -d
```

### Maintenance

```bash
cd docker
./docker-helper.sh cleanup
```

## Configuration Files

- Nginx:      `docker/nginx.conf`
- Prometheus: `docker/prometheus.yml`
- .dockerignore: `docker/.dockerignore`

## Environment Variables

### Required

- `GEMINI_API_KEY`: Your Google Gemini API key

### Optional

- `GEMINI_MODEL`: AI model to use (default: gemini-2.5-pro)
- `GEMINI_MAX_TOKENS`: Maximum tokens for AI responses (default: 2048)
- `GEMINI_TEMPERATURE`: AI creativity level (default: 0.3)
- `ENABLE_LOG_OPTIMIZATION`: Enable log optimization (default: true)
- `MAX_INPUT_TOKENS`: Maximum input tokens (default: 30000)
- `MAX_LOG_ENTRIES`: Maximum log entries to process (default: 1000)
- `SAMPLE_SIZE`: Sample size for analysis (default: 500)
- `LOG_LEVEL`: Logging level (default: INFO)
- `SECRET_KEY`: Flask secret key (default: auto-generated)

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the ports
   lsof -i :8000
   lsof -i :4000
   
   # Stop conflicting services or change ports in docker-compose.yml
   ```

2. **Permission Issues**
   ```bash
   # Fix volume permissions
   sudo chown -R $USER:$USER data/ uploads/ logs/
   ```

3. **API Key Issues**
   ```bash
   # Check if API key is set
   docker-compose exec backend env | grep GEMINI_API_KEY
   
   # Restart with new environment
   docker-compose down
   docker-compose up --build
   ```

4. **Memory Issues**
   ```bash
   # Increase Docker memory limit in Docker Desktop
   # Or use resource limits in docker-compose.yml
   ```

### Health Checks

The backend includes health checks:

```bash
# Check service health
docker-compose ps

# Manual health check
curl http://localhost:8000/health
```

### Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
```

## Production Deployment

### Using Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml log-investigator

# Scale services
docker service scale log-investigator_backend=3
```

### Using Kubernetes

1. Create Kubernetes manifests from docker-compose.yml
2. Apply to your cluster:
   ```bash
   kubectl apply -f k8s/
   ```

### Reverse Proxy Setup

For production, consider using Nginx or Traefik:

```yaml
# Add to docker-compose.yml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
  depends_on:
    - frontend
    - backend
```

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Secrets**: Use Docker secrets for sensitive data
3. **Network**: Use internal networks for service communication
4. **Volumes**: Mount volumes with appropriate permissions
5. **Updates**: Regularly update base images and dependencies

## Performance Optimization

1. **Multi-stage builds**: Already implemented for smaller images
2. **Caching**: Use Docker layer caching effectively
3. **Resource limits**: Set appropriate CPU/memory limits
4. **Health checks**: Monitor service health
5. **Logging**: Implement proper log rotation

## Monitoring

### Basic Monitoring

```bash
# Resource usage
docker stats

# Service status
docker-compose ps

# Health checks
curl http://localhost:8000/health
```

### Advanced Monitoring

Consider adding:
- Prometheus for metrics
- Grafana for visualization
- ELK stack for log aggregation
- Jaeger for distributed tracing

## Backup and Recovery

### Data Backup

```bash
# Backup volumes
docker run --rm -v log-investigator_data:/data -v $(pwd):/backup alpine tar czf /backup/data-backup.tar.gz -C /data .

# Restore volumes
docker run --rm -v log-investigator_data:/data -v $(pwd):/backup alpine tar xzf /backup/data-backup.tar.gz -C /data
```

### Configuration Backup

```bash
# Backup configuration
cp .env .env.backup
cp docker-compose.yml docker-compose.yml.backup
```

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review Docker and Docker Compose logs
3. Verify environment variables and configuration
4. Check the main project README for additional information 