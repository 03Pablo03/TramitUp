# TramitUp Development Makefile

.PHONY: help install-frontend install-backend install dev dev-frontend dev-backend build test test-frontend test-backend lint lint-frontend lint-backend format format-frontend format-backend clean docker-build docker-up docker-down

# Default target
help:
	@echo "TramitUp Development Commands"
	@echo "============================="
	@echo ""
	@echo "Setup:"
	@echo "  install           Install all dependencies"
	@echo "  install-frontend  Install frontend dependencies"
	@echo "  install-backend   Install backend dependencies"
	@echo ""
	@echo "Development:"
	@echo "  dev              Start both frontend and backend"
	@echo "  dev-frontend     Start frontend development server"
	@echo "  dev-backend      Start backend development server"
	@echo ""
	@echo "Build:"
	@echo "  build            Build both frontend and backend"
	@echo ""
	@echo "Testing:"
	@echo "  test             Run all tests"
	@echo "  test-frontend    Run frontend tests"
	@echo "  test-backend     Run backend tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint             Run linting for both projects"
	@echo "  lint-frontend    Run frontend linting"
	@echo "  lint-backend     Run backend linting"
	@echo "  format           Format code for both projects"
	@echo "  format-frontend  Format frontend code"
	@echo "  format-backend   Format backend code"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build     Build Docker images"
	@echo "  docker-up        Start services with Docker Compose"
	@echo "  docker-down      Stop Docker services"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean            Clean build artifacts and caches"

# Installation
install: install-frontend install-backend

install-frontend:
	cd frontend && npm install

install-backend:
	cd backend && pip install -r requirements.txt

# Development
dev:
	@echo "Starting TramitUp development servers..."
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@echo "Press Ctrl+C to stop both servers"
	@(trap 'kill 0' SIGINT; \
		cd frontend && npm run dev & \
		cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 & \
		wait)

dev-frontend:
	cd frontend && npm run dev

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Build
build:
	@echo "Building frontend..."
	cd frontend && npm run build
	@echo "Frontend build complete!"

# Testing
test: test-frontend test-backend

test-frontend:
	cd frontend && npm run test

test-backend:
	cd backend && python -m pytest

# Linting
lint: lint-frontend lint-backend

lint-frontend:
	cd frontend && npm run lint

lint-backend:
	cd backend && flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics

# Formatting
format: format-frontend format-backend

format-frontend:
	cd frontend && npx prettier --write .

format-backend:
	cd backend && black app && isort app

# Docker
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

# Maintenance
clean:
	@echo "Cleaning build artifacts..."
	rm -rf frontend/.next
	rm -rf frontend/node_modules/.cache
	rm -rf backend/__pycache__
	rm -rf backend/.pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Clean complete!"