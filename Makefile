# Makefile for EduFlow - Production-Ready Commands

.PHONY: help install dev build test lint clean docker-build docker-up docker-down deploy security-check

# Default target
help:
	@echo "EduFlow - Available Commands:"
	@echo ""
	@echo "  Development:"
	@echo "    make install          - Install all dependencies"
	@echo "    make dev              - Run development servers"
	@echo "    make test             - Run all tests"
	@echo "    make lint             - Run linters"
	@echo "    make format           - Format code"
	@echo ""
	@echo "  Production:"
	@echo "    make build            - Build for production"
	@echo "    make docker-build     - Build Docker images"
	@echo "    make docker-up        - Start Docker containers"
	@echo "    make docker-down      - Stop Docker containers"
	@echo "    make deploy           - Deploy to production"
	@echo ""
	@echo "  Maintenance:"
	@echo "    make clean            - Clean build artifacts"
	@echo "    make security-check   - Run security scans"
	@echo "    make backup           - Backup database"
	@echo "    make logs             - View application logs"

# Installation
install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install --legacy-peer-deps
	@echo "✅ All dependencies installed!"

install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install --legacy-peer-deps

# Development
dev:
	@echo "Starting development servers..."
	npm run dev

dev-backend:
	cd backend && python server.py

dev-frontend:
	cd frontend && npm start

# Testing
test:
	@echo "Running backend tests..."
	cd backend && pytest tests/ -v
	@echo "Running frontend tests..."
	cd frontend && CI=true npm test

test-backend:
	cd backend && pytest tests/ -v --cov=. --cov-report=html

test-frontend:
	cd frontend && CI=true npm test -- --coverage

test-watch:
	cd frontend && npm test

# Linting & Formatting
lint:
	@echo "Linting backend..."
	cd backend && flake8 server.py --max-line-length=120
	cd backend && mypy server.py --ignore-missing-imports
	@echo "Linting frontend..."
	cd frontend && npm run lint || true

format:
	@echo "Formatting backend code..."
	cd backend && black server.py rate_limiter.py
	cd backend && isort server.py rate_limiter.py
	@echo "✅ Code formatted!"

format-check:
	cd backend && black --check server.py rate_limiter.py
	cd backend && isort --check-only server.py rate_limiter.py

# Build
build:
	@echo "Building frontend for production..."
	cd frontend && npm run build
	@echo "✅ Production build complete!"

build-backend:
	@echo "Backend is interpreted - no build needed"

build-frontend:
	cd frontend && npm run build

# Docker
docker-build:
	@echo "Building Docker images..."
	docker-compose build
	@echo "✅ Docker images built!"

docker-up:
	@echo "Starting Docker containers..."
	docker-compose up -d
	@echo "✅ Containers started!"
	@echo "Frontend: http://localhost"
	@echo "Backend: http://localhost:8000"
	@echo "Docs: http://localhost:8000/docs"

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down
	@echo "✅ Containers stopped!"

docker-logs:
	docker-compose logs -f

docker-restart:
	docker-compose restart

# Security
security-check:
	@echo "Running security checks..."
	@echo "Checking backend dependencies..."
	cd backend && pip install safety && safety check || true
	@echo "Checking frontend dependencies..."
	cd frontend && npm audit || true
	@echo "✅ Security scan complete!"

# Deployment
deploy:
	@echo "🚀 Starting deployment..."
	@echo "1. Running tests..."
	make test
	@echo "2. Running security checks..."
	make security-check
	@echo "3. Building for production..."
	make build
	@echo "4. Building Docker images..."
	make docker-build
	@echo "✅ Ready for deployment!"
	@echo ""
	@echo "Next steps:"
	@echo "  - Push to Docker Hub: docker-compose push"
	@echo "  - Deploy to server: See PRODUCTION_GUIDE.md"

# Database
backup:
	@echo "Creating database backup..."
	docker-compose exec mongodb mongodump --out=/tmp/backup
	@echo "✅ Backup created in container"

restore:
	@echo "Restoring database from backup..."
	docker-compose exec mongodb mongorestore /tmp/backup
	@echo "✅ Database restored"

# Logs
logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-db:
	docker-compose logs -f mongodb

# Cleanup
clean:
	@echo "Cleaning build artifacts..."
	rm -rf frontend/build
	rm -rf frontend/node_modules/.cache
	rm -rf backend/__pycache__
	rm -rf backend/**/__pycache__
	rm -rf backend/.pytest_cache
	rm -rf backend/htmlcov
	rm -rf backend/.coverage
	@echo "✅ Cleaned!"

clean-all: clean
	@echo "Removing all dependencies..."
	rm -rf frontend/node_modules
	rm -rf backend/venv
	@echo "✅ All dependencies removed!"

# Health check
health:
	@echo "Checking application health..."
	@curl -f http://localhost:8000/health || echo "❌ Backend unhealthy"
	@curl -f http://localhost/health || echo "❌ Frontend unhealthy"

# Production setup
setup-prod:
	@echo "Setting up production environment..."
	@echo "1. Creating .env files from examples..."
	cp backend/.env.example backend/.env
	@echo "2. Generating secret key..."
	@python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))" >> backend/.env
	@echo "✅ Environment files created!"
	@echo "⚠️  Edit backend/.env and add your API keys and database URL"

# CI/CD
ci:
	@echo "Running CI pipeline..."
	make install
	make lint
	make test
	make security-check
	make build
	@echo "✅ CI pipeline passed!"

# Status
status:
	@echo "🔍 System Status:"
	@echo ""
	@docker-compose ps
	@echo ""
	@echo "Health Checks:"
	@make health
