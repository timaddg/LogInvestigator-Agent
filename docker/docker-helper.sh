#!/bin/bash

# Log Investigator Docker Helper Script
# This script provides common Docker operations for the Log Investigator project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to check if .env file exists
check_env() {
    if [ ! -f "../.env" ]; then
        print_warning ".env file not found in parent directory. Creating from template..."
        if [ -f "../env.example" ]; then
            cp ../env.example ../.env
            print_status "Created .env file from template. Please edit it with your API key."
        else
            print_error "env.example not found in parent directory. Please create a .env file manually."
            exit 1
        fi
    fi
}

# Function to build and start services
start() {
    print_header "Starting Log Investigator with Docker"
    check_docker
    check_env
    
    print_status "Building and starting services..."
    docker-compose up --build -d
    
    print_status "Services started successfully!"
    print_status "Frontend: http://localhost:4000"
    print_status "Backend:  http://localhost:8000"
    print_status "Health:   http://localhost:8000/health"
}

# Function to stop services
stop() {
    print_header "Stopping Log Investigator"
    print_status "Stopping services..."
    docker-compose down
    print_status "Services stopped successfully!"
}

# Function to restart services
restart() {
    print_header "Restarting Log Investigator"
    stop
    start
}

# Function to view logs
logs() {
    print_header "Viewing Logs"
    if [ -z "$1" ]; then
        print_status "Showing all logs (Ctrl+C to exit)..."
        docker-compose logs -f
    else
        print_status "Showing logs for service: $1"
        docker-compose logs -f "$1"
    fi
}

# Function to check service status
status() {
    print_header "Service Status"
    docker-compose ps
    
    echo ""
    print_header "Health Check"
    if curl -s http://localhost:8000/health > /dev/null; then
        print_status "Backend is healthy"
    else
        print_error "Backend health check failed"
    fi
}

# Function to clean up
cleanup() {
    print_header "Cleaning Up Docker Resources"
    print_warning "This will remove all containers, networks, and volumes!"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Stopping and removing containers..."
        docker-compose down -v
        print_status "Removing unused images..."
        docker image prune -f
        print_status "Removing unused volumes..."
        docker volume prune -f
        print_status "Cleanup completed!"
    else
        print_status "Cleanup cancelled."
    fi
}

# Function to rebuild specific service
rebuild() {
    if [ -z "$1" ]; then
        print_error "Please specify a service to rebuild (backend or frontend)"
        exit 1
    fi
    
    print_header "Rebuilding Service: $1"
    print_status "Rebuilding $1..."
    docker-compose build "$1"
    print_status "Restarting $1..."
    docker-compose up -d "$1"
    print_status "Service $1 rebuilt and restarted!"
}

# Function to show help
show_help() {
    echo "Log Investigator Docker Helper Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     Build and start all services"
    echo "  stop      Stop all services"
    echo "  restart   Restart all services"
    echo "  logs      Show logs (all services or specific service)"
    echo "  status    Show service status and health"
    echo "  cleanup   Clean up all Docker resources"
    echo "  rebuild   Rebuild a specific service (backend/frontend)"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start                    # Start all services"
    echo "  $0 logs                     # Show all logs"
    echo "  $0 logs backend             # Show backend logs only"
    echo "  $0 rebuild frontend         # Rebuild frontend service"
    echo ""
}

# Main script logic
case "${1:-help}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs "$2"
        ;;
    status)
        status
        ;;
    cleanup)
        cleanup
        ;;
    rebuild)
        rebuild "$2"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac 