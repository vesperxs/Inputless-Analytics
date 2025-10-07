# Inputless Analytics - Makefile
# Development and deployment commands

.PHONY: help install test security format lint clean build deploy

# Default target
help:
	@echo "Inputless Analytics - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  install     Install all dependencies"
	@echo "  test        Run all tests"
	@echo "  lint        Run linting checks"
	@echo "  format      Format code"
	@echo "  security    Run security checks"
	@echo ""
	@echo "Docker:"
	@echo "  build       Build Docker images"
	@echo "  up          Start development environment"
	@echo "  down        Stop development environment"
	@echo "  logs        View application logs"
	@echo ""
	@echo "Infrastructure:"
	@echo "  terraform-init    Initialize Terraform"
	@echo "  terraform-plan    Plan Terraform changes"
	@echo "  terraform-apply   Apply Terraform changes"
	@echo "  terraform-destroy Destroy infrastructure"
	@echo ""
	@echo "Utilities:"
	@echo "  clean       Clean up temporary files"
	@echo "  docs        Generate documentation"

# Development Commands
install:
	@echo "Installing dependencies..."
	cd backend && pip install -r requirements.txt
	cd frontend && npm install
	@echo "Dependencies installed successfully!"

test:
	@echo "Running tests..."
	cd backend && python manage.py test
	cd frontend && npm test
	@echo "All tests completed!"

lint:
	@echo "Running linting checks..."
	cd backend && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	cd backend && flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	cd frontend && npm run lint
	@echo "Linting completed!"

format:
	@echo "Formatting code..."
	cd backend && black .
	cd backend && isort .
	cd frontend && npm run format
	@echo "Code formatting completed!"

security:
	@echo "Running security checks..."
	cd backend && bandit -r . -f json -o bandit-report.json
	cd backend && safety check
	cd frontend && npm audit
	@echo "Security checks completed!"

# Docker Commands
build:
	@echo "Building Docker images..."
	docker-compose build
	@echo "Docker images built successfully!"

up:
	@echo "Starting development environment..."
	docker-compose up -d
	@echo "Development environment started!"

down:
	@echo "Stopping development environment..."
	docker-compose down
	@echo "Development environment stopped!"

logs:
	@echo "Viewing application logs..."
	docker-compose logs -f

# Infrastructure Commands
terraform-init:
	@echo "Initializing Terraform..."
	cd terraform && terraform init
	@echo "Terraform initialized!"

terraform-plan:
	@echo "Planning Terraform changes..."
	cd terraform && terraform plan
	@echo "Terraform plan completed!"

terraform-apply:
	@echo "Applying Terraform changes..."
	cd terraform && terraform apply
	@echo "Terraform apply completed!"

terraform-destroy:
	@echo "Destroying infrastructure..."
	cd terraform && terraform destroy
	@echo "Infrastructure destroyed!"

# Documentation
docs:
	@echo "Generating documentation..."
	cd backend && sphinx-build -b html docs/source docs/build
	@echo "Documentation generated!"

# Utilities
clean:
	@echo "Cleaning up temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type f -name "*.log" -delete
	@echo "Cleanup completed!"

# Development environment setup
dev-setup: install
	@echo "Setting up development environment..."
	cd backend && python manage.py migrate
	cd backend && python manage.py createsuperuser --noinput --username admin --email admin@example.com || echo "Superuser already exists"
	@echo "Development environment setup completed!"

# Production deployment
deploy-staging:
	@echo "Deploying to staging..."
	cd terraform && terraform apply -var-file="staging.tfvars"
	@echo "Staging deployment completed!"

deploy-production:
	@echo "Deploying to production..."
	cd terraform && terraform apply -var-file="production.tfvars"
	@echo "Production deployment completed!"

# Health checks
health-check:
	@echo "Running health checks..."
	curl -f http://localhost:3000/health || echo "Application health check failed"
	curl -f http://localhost:3060 || echo "Grafana health check failed"
	curl -f http://localhost:9090 || echo "Prometheus health check failed"
	@echo "Health checks completed!"

# Database operations
db-migrate:
	@echo "Running database migrations..."
	docker-compose exec Web python manage.py migrate
	@echo "Database migrations completed!"

db-shell:
	@echo "Opening database shell..."
	docker-compose exec Web python manage.py dbshell

# Backup operations
backup:
	@echo "Creating backup..."
	docker-compose exec Web python manage.py dumpdata > backup_$(shell date +%Y%m%d_%H%M%S).json
	@echo "Backup created!"

# Monitoring
monitor:
	@echo "Starting monitoring..."
	docker-compose exec Web python manage.py runserver 0.0.0.0:8000 &
	@echo "Monitoring started!"

# Quick start for new developers
quickstart: install dev-setup up
	@echo "Quick start completed!"
	@echo "Application is running at: http://localhost:3000"
	@echo "Admin panel: http://localhost:3000/admin/"
	@echo "Grafana: http://localhost:3060"
	@echo "Prometheus: http://localhost:9090"
