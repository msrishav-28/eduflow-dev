#!/bin/bash

# Production Setup Script for EduFlow
# This script helps set up a production environment

set -e  # Exit on error

echo "🚀 EduFlow Production Setup"
echo "=============================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}❌ Please do not run as root${NC}"
    exit 1
fi

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites satisfied${NC}"
echo ""

# Environment configuration
echo "🔧 Setting up environment configuration..."

# Backend .env
if [ ! -f backend/.env ]; then
    echo "Creating backend/.env from template..."
    cp backend/.env.example backend/.env
    
    # Generate secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    echo "SECRET_KEY=$SECRET_KEY" >> backend/.env
    
    echo -e "${GREEN}✅ Backend .env created${NC}"
    echo -e "${YELLOW}⚠️  Please edit backend/.env and add:${NC}"
    echo "   - MongoDB connection URL"
    echo "   - LLM API keys (at least one)"
    echo "   - CORS origins (your production domain)"
    echo "   - ALLOWED_HOSTS (your production domain)"
    echo ""
    
    read -p "Press Enter after editing backend/.env..."
else
    echo -e "${YELLOW}ℹ️  backend/.env already exists${NC}"
fi

# Frontend .env.production
if [ ! -f frontend/.env.production ]; then
    echo "Creating frontend/.env.production..."
    cat > frontend/.env.production << EOF
REACT_APP_BACKEND_URL=https://api.yourdomain.com
REACT_APP_ENV=production
EOF
    echo -e "${GREEN}✅ Frontend .env.production created${NC}"
    echo -e "${YELLOW}⚠️  Please edit frontend/.env.production and set your backend URL${NC}"
    echo ""
    
    read -p "Press Enter after editing frontend/.env.production..."
else
    echo -e "${YELLOW}ℹ️  frontend/.env.production already exists${NC}"
fi

# SSL Certificate setup
echo ""
echo "🔒 SSL Certificate Setup"
echo "========================"
echo "For production, you need SSL certificates."
echo ""
echo "Options:"
echo "  1. Use Let's Encrypt (recommended, free)"
echo "  2. Use existing certificates"
echo "  3. Skip (set up later)"
echo ""
read -p "Choose option (1-3): " ssl_option

case $ssl_option in
    1)
        echo "Let's Encrypt setup..."
        echo "Run after deployment:"
        echo "  sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com"
        ;;
    2)
        echo "Place your certificates in:"
        echo "  - /etc/ssl/certs/yourdomain.crt"
        echo "  - /etc/ssl/private/yourdomain.key"
        ;;
    3)
        echo "Skipping SSL setup"
        ;;
esac

# Docker setup
echo ""
echo "🐳 Docker Setup"
echo "==============="
echo "Building Docker images..."

if docker-compose build; then
    echo -e "${GREEN}✅ Docker images built successfully${NC}"
else
    echo -e "${RED}❌ Docker build failed${NC}"
    exit 1
fi

# Start services
echo ""
echo "🚀 Starting Services"
echo "===================="
read -p "Start services now? (y/n): " start_services

if [ "$start_services" = "y" ]; then
    docker-compose up -d
    
    echo ""
    echo "Waiting for services to be ready..."
    sleep 10
    
    # Health checks
    echo ""
    echo "🏥 Health Checks"
    echo "================"
    
    # Backend health
    if curl -f http://localhost:8000/health &> /dev/null; then
        echo -e "${GREEN}✅ Backend is healthy${NC}"
    else
        echo -e "${RED}❌ Backend is not responding${NC}"
    fi
    
    # Frontend health
    if curl -f http://localhost/health &> /dev/null; then
        echo -e "${GREEN}✅ Frontend is healthy${NC}"
    else
        echo -e "${RED}❌ Frontend is not responding${NC}"
    fi
fi

# Security reminders
echo ""
echo "🔐 Security Checklist"
echo "====================="
echo "Before going to production, ensure:"
echo "  □ Changed all default passwords"
echo "  □ Added production domain to CORS_ORIGINS"
echo "  □ Added production domain to ALLOWED_HOSTS"
echo "  □ Enabled HTTPS/SSL"
echo "  □ Set up firewall rules"
echo "  □ Configured database backups"
echo "  □ Set up monitoring"
echo "  □ Reviewed SECURITY.md"

# Next steps
echo ""
echo "📝 Next Steps"
echo "============="
echo "1. Review configuration files"
echo "2. Set up SSL certificates"
echo "3. Configure domain DNS"
echo "4. Set up monitoring (see PRODUCTION_GUIDE.md)"
echo "5. Test the application thoroughly"
echo ""
echo "📚 Documentation:"
echo "  - PRODUCTION_GUIDE.md - Complete production guide"
echo "  - SECURITY.md - Security best practices"
echo "  - README.md - General documentation"
echo ""
echo "🎉 Setup complete!"
echo ""
echo "Access your application:"
echo "  - Frontend: http://localhost (or your domain with SSL)"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "View logs:"
echo "  docker-compose logs -f"
echo ""
