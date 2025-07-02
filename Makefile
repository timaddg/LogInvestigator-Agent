# Log Investigator Makefile
# Provides convenient commands for Docker operations

.PHONY: help build up down restart logs status clean dev prod test

# Default target
help:
	@echo "Log Investigator - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make dev      - Start development environment"
	@echo "  make build    - Build Docker images"
	@echo "  make up       - Start services"
	@echo "  make down     - Stop services"
	@echo "  make restart  - Restart services"
	@echo "  make logs     - Show logs"
	@echo "  make status   - Show service status"
	@echo ""
	@echo "Production:"
	@echo "  make prod     - Start production environment"
	@echo "  make prod-up  - Start production services"
	@echo "  make prod-down - Stop production services"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean    - Clean up Docker resources"
	@echo "  make test     - Run tests"
	@echo "  make shell    - Open shell in backend container"
	@echo ""

# Development environment
dev: build up

build:
	@echo "Building Docker images..."
	docker-compose build

up:
	@echo "Starting development services..."
	docker-compose up -d
	@echo "Services started!"
	@echo "Frontend: http://localhost:4000"
	@echo "Backend:  http://localhost:8000"
	@echo "Health:   http://localhost:8000/health"

down:
	@echo "Stopping services..."
	docker-compose down

restart: down up

logs:
	@echo "Showing logs (Ctrl+C to exit)..."
	docker-compose logs -f

status:
	@echo "Service Status:"
	docker-compose ps
	@echo ""
	@echo "Health Check:"
	@curl -s http://localhost:8000/health || echo "Backend not responding"

# Production environment
prod: prod-build prod-up

prod-build:
	@echo "Building production images..."
	docker-compose -f docker-compose.prod.yml build

prod-up:
	@echo "Starting production services..."
	docker-compose -f docker-compose.prod.yml up -d
	@echo "Production services started!"
	@echo "Application: http://localhost"
	@echo "Grafana:     http://localhost:3000"
	@echo "Prometheus:  http://localhost:9090"

prod-down:
	@echo "Stopping production services..."
	docker-compose -f docker-compose.prod.yml down

prod-restart: prod-down prod-up

prod-logs:
	@echo "Showing production logs (Ctrl+C to exit)..."
	docker-compose -f docker-compose.prod.yml logs -f

# Maintenance
clean:
	@echo "Cleaning up Docker resources..."
	docker-compose down -v
	docker system prune -f
	docker volume prune -f
	@echo "Cleanup completed!"

test:
	@echo "Running tests..."
	docker-compose exec backend python -m pytest tests/ -v

shell:
	@echo "Opening shell in backend container..."
	docker-compose exec backend /bin/bash

# Environment setup
setup:
	@echo "Setting up environment..."
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		cp env.example .env; \
		echo "Please edit .env file with your API key"; \
	else \
		echo ".env file already exists"; \
	fi

# Quick commands
start: dev
stop: down
rebuild: build restart 