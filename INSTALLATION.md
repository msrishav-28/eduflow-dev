# Installation Guide

Complete setup guide for EduFlow - all versions (V1, V2, V3).

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.9+
- Node.js 18+ (for frontend)
- MongoDB (optional for V1/V2, required for V3 auth/gamification)

### Basic Setup

```bash
# 1. Install backend dependencies
cd backend
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env

# Edit .env - add at minimum:
# GEMINI_API_KEY=your-api-key-here

# 3. Start backend
python server.py

# 4. Install frontend (separate terminal)
cd frontend
npm install
npm start
```

---

## 📦 Detailed Installation

### Backend Setup

#### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Core dependencies:**
- FastAPI, Uvicorn
- Pydantic
- Motor (MongoDB async driver)
- LLM providers (Google Gemini, OpenAI, Anthropic)
- File processing (PyPDF2, python-docx)
- Authentication (python-jose, passlib, bcrypt)

#### 2. Environment Configuration

```bash
cp .env.example .env
```

**Required variables:**
```bash
# LLM Provider (choose at least one)
GEMINI_API_KEY=your-gemini-api-key
# OR
OPENAI_API_KEY=your-openai-api-key
# OR
ANTHROPIC_API_KEY=your-anthropic-api-key
```

**Optional for V3 features:**
```bash
# MongoDB (required for auth & gamification)
MONGO_URL=mongodb://localhost:27017
DB_NAME=eduflow

# Authentication
SECRET_KEY=your-super-secret-key-change-this

# Environment
ENV=development
DEBUG=True
```

**Optional for production:**
```bash
CORS_ORIGINS=http://localhost:3000
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### 3. MongoDB Setup (Optional/Required)

**Option A: Docker (Easiest)**
```bash
docker run -d -p 27017:27017 --name mongodb mongo
```

**Option B: MongoDB Atlas (Free Cloud)**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Add to .env: `MONGO_URL=mongodb+srv://...`

**Option C: Local Installation**
- Download from https://www.mongodb.com/try/download/community
- Install and run `mongod`

#### 4. Generate Secret Key (for V3)

```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Add to .env
SECRET_KEY=generated-key-here
```

#### 5. Start Backend Server

```bash
python server.py
```

**Verify startup messages:**
```
✅ MongoDB configured (or "not configured" if optional)
✅ LLM Provider: gemini
✅ Enhanced v2 endpoints loaded
✅ V3 endpoints loaded (if MongoDB available)
```

Server runs on: http://localhost:8000

---

### Frontend Setup

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

#### 2. Configure Environment

Create `.env` file:
```bash
# For local development
REACT_APP_BACKEND_URL=http://localhost:8000

# For production (leave empty if deployed together)
REACT_APP_BACKEND_URL=
```

#### 3. Start Development Server

```bash
npm start
```

Frontend runs on: http://localhost:3000

#### 4. Build for Production

```bash
npm run build
```

Build output in `frontend/build/`

---

## 🎮 Feature-Specific Setup

### V1 Features (Basic AI)
**Requirements:** LLM API key only
```bash
GEMINI_API_KEY=your-key
```
**Available:** Q&A, Basic summarizer, Basic MCQ, Basic code explainer

### V2 Features (Enhanced)
**Requirements:** LLM API key + file processing libraries
```bash
# Already in requirements.txt
pip install PyPDF2 python-docx python-multipart
```
**Available:** File upload, 5 summary styles, difficulty-based MCQs

### V3 Features (Full Platform)
**Requirements:** All of above + MongoDB
```bash
# Install auth dependencies
pip install python-jose[cryptography] passlib[bcrypt]

# Setup MongoDB
docker run -d -p 27017:27017 mongo

# Configure
MONGO_URL=mongodb://localhost:27017
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
```
**Available:** Authentication, gamification, advanced code analyzer

---

## 🧪 Verify Installation

### Test Backend

```bash
# Health check
curl http://localhost:8000/health

# API root
curl http://localhost:8000/api/

# Test Q&A
curl -X POST http://localhost:8000/api/qa \
  -H "Content-Type: application/json" \
  -d '{"question":"What is AI?","depth":"concise"}'
```

### Test V2 Features

```bash
# Test file upload summarizer
echo "Test content" > test.txt
curl -X POST http://localhost:8000/api/v2/summarize \
  -F "file=@test.txt" \
  -F "style=short_notes" \
  -F "max_points=3"
```

### Test V3 Features

```bash
# Test signup
curl -X POST http://localhost:8000/api/v3/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123"}'

# Test code analyzer
curl -X POST http://localhost:8000/api/v3/code/analyze \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "code=def hello(): print('test')" \
  -F "language=python"
```

---

## 🐳 Docker Installation

### Using Docker Compose

```bash
# Build and start all services
docker-compose up -d

# Verify
docker-compose ps
docker-compose logs
```

### Manual Docker Build

**Backend:**
```bash
cd backend
docker build -t eduflow-backend .
docker run -p 8000:8000 eduflow-backend
```

**Frontend:**
```bash
cd frontend
docker build -t eduflow-frontend .
docker run -p 80:80 eduflow-frontend
```

---

## 🔧 Troubleshooting

### "No LLM API key configured"
**Solution:** Add at least one API key to `.env`
```bash
GEMINI_API_KEY=your-key
```

### "MongoDB connection failed"
**Solution:** 
- Check MongoDB is running: `docker ps | grep mongodb`
- Or disable: `MONGO_URL=` (empty)
- V1/V2 work without MongoDB

### "ModuleNotFoundError"
**Solution:** Install missing dependencies
```bash
pip install -r requirements.txt
```

### "Port already in use"
**Solution:** Change port in `.env`
```bash
PORT=8001
```

### Frontend can't connect to backend
**Solution:** Check CORS and backend URL
```bash
# Backend .env
CORS_ORIGINS=http://localhost:3000

# Frontend .env
REACT_APP_BACKEND_URL=http://localhost:8000
```

---

## 📊 System Requirements

### Minimum
- CPU: 2 cores
- RAM: 2GB
- Disk: 1GB
- OS: Windows, macOS, Linux

### Recommended (Production)
- CPU: 4+ cores
- RAM: 4GB+
- Disk: 5GB+
- MongoDB: 1GB+ storage

---

## ⚡ Quick Commands Reference

```bash
# Install everything
make install

# Run development
make dev

# Run tests
make test

# Build Docker images
make docker-build

# Deploy
make docker-up

# Check health
make health

# View logs
make logs

# Clean up
make clean
```

---

## 🚀 Ready to Deploy?

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment guides (Vercel, Docker, Cloud providers).

---

**Installation complete!** Your EduFlow app is ready to use. 🎉
