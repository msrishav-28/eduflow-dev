# Changelog

All notable changes to EduFlow are documented in this file.

---

## [3.0.0] - 2024-12 - Full Platform Release

### Added
- **Authentication System**
  - Email + password signup/login
  - JWT token-based authentication
  - Secure password hashing with bcrypt
  - User profiles

- **Gamification System**
  - Point rewards for all activities
  - 9 achievement badges
  - 5-level progression system
  - Monthly and all-time leaderboards
  - Daily activity streak tracking
  - Point-based feature unlocks

- **Advanced Code Analyzer**
  - Support for 18 programming languages
  - Quality scoring (0-100) with 5-category breakdown
  - Error detection (syntax, logic, style, security, performance)
  - Line-by-line code corrections
  - Performance optimization suggestions
  - Security vulnerability detection
  - Drag & drop file upload

- **Backend Architecture**
  - Modular service-based architecture
  - `auth.py` - Authentication service
  - `gamification.py` - Gamification service
  - `code_analyzer.py` - Code analysis service
  - `models/` directory with data models

- **API Endpoints**
  - `/api/v3/auth/*` - Authentication endpoints (3)
  - `/api/v3/gamification/*` - Gamification endpoints (2)
  - `/api/v3/code/*` - Advanced code analysis (2)

### Changed
- MongoDB now optional for basic features, required for V3 auth/gamification
- Backend split into modular services for better maintainability
- Enhanced error handling throughout

---

## [2.0.0] - 2024-11 - Enhanced Features

### Added
- **File Upload Support**
  - Drag & drop interface
  - PDF file processing (PyPDF2)
  - Word document processing (python-docx)
  - Text file processing

- **Enhanced Summarizer**
  - 5 summary styles (short_notes, long_notes, balanced, bullet_points, detailed)
  - Support for documents up to 50,000 characters
  - Smart chunking for large documents
  - File upload endpoint `/api/v2/summarize`

- **Enhanced MCQ Generator**
  - 3 difficulty levels (easy, medium, hard)
  - 4 question types (factual, conceptual, application, mixed)
  - File upload support
  - Up to 20 questions per set
  - File upload endpoint `/api/v2/mcq`

- **Backend Modules**
  - `llm_service.py` - LLM provider abstraction
  - `file_processor.py` - File upload handling
  - `endpoints.py` - V2 API endpoints

### Changed
- Increased max text length from 10K to 50K characters
- Improved LLM prompt engineering for better results

---

## [1.0.0] - 2024-10 - Production Ready

### Added
- **Production Environment**
  - Environment-based configuration (development/production)
  - `.env.example` template file
  - Production logging configuration
  - Health check endpoints (`/health`, `/readiness`)

- **Security Features**
  - Request ID tracking
  - Global exception handling
  - Input validation with Pydantic
  - Rate limiting middleware (60/min, 1000/hour)
  - CORS protection
  - Trusted Host middleware
  - GZip compression

- **Docker Support**
  - Multi-stage Dockerfile for backend
  - Nginx-based Dockerfile for frontend
  - Docker Compose configuration
  - Health checks in containers
  - Non-root container users

- **CI/CD**
  - GitHub Actions workflow
  - Automated testing
  - Linting and formatting checks
  - Security scanning with Trivy
  - Docker image building

- **Documentation**
  - Production deployment guide
  - Security documentation
  - Makefile for common operations
  - Setup scripts

### Changed
- MongoDB connection now optional with graceful degradation
- Startup/shutdown event handling improved
- Better error messages in production vs development

---

## [0.9.0] - 2024-09 - Initial Release

### Added
- **Core AI Features**
  - Q&A system with depth control (concise, balanced, detailed)
  - Text summarizer with bullet points
  - MCQ generator for any topic
  - Code explainer for multiple languages

- **LLM Provider Support**
  - Google Gemini integration
  - OpenAI GPT integration
  - Anthropic Claude integration
  - Automatic provider selection and fallback

- **API Endpoints**
  - `POST /api/qa` - Question answering
  - `POST /api/summarize` - Text summarization
  - `POST /api/mcq` - MCQ generation
  - `POST /api/explain-code` - Code explanation

- **Frontend**
  - React 19 application
  - Tailwind CSS styling
  - Radix UI components
  - Framer Motion animations
  - Responsive design

- **Backend**
  - FastAPI framework
  - MongoDB for data persistence
  - Async/await architecture
  - Input validation

---

## Version Summary

| Version | Release Date | Key Features |
|---------|--------------|--------------|
| **3.0.0** | 2024-12 | Auth, Gamification, Advanced Code Analyzer |
| **2.0.0** | 2024-11 | File Upload, Enhanced Features |
| **1.0.0** | 2024-10 | Production Ready, Docker, CI/CD |
| **0.9.0** | 2024-09 | Initial Release, Core AI Features |

---

## Feature Timeline

### V3 (Current)
- ✅ User authentication
- ✅ Points and badges
- ✅ Leaderboards
- ✅ Advanced code analysis
- ✅ Quality scoring
- ✅ Feature unlocks

### V2
- ✅ File upload (PDF, Word, Text)
- ✅ Multiple summary styles
- ✅ Difficulty levels for MCQs
- ✅ Large document support

### V1
- ✅ Production environment
- ✅ Security features
- ✅ Docker deployment
- ✅ CI/CD pipeline

### V0.9
- ✅ Q&A system
- ✅ Summarizer
- ✅ MCQ generator
- ✅ Code explainer

---

## Breaking Changes

### V3.0.0
- MongoDB now required for authentication and gamification features
- New environment variable required: `SECRET_KEY`
- Password requirements enforced (min 8 chars, uppercase, lowercase, digit)

### V2.0.0
- File upload uses `multipart/form-data` instead of JSON
- New dependencies required: `PyPDF2`, `python-docx`, `python-multipart`

### V1.0.0
- Environment variables moved to `.env` file
- MongoDB connection URL format changed
- API docs disabled in production by default

---

## Upgrade Guide

### V2 to V3
```bash
# 1. Install new dependencies
pip install python-jose[cryptography] passlib[bcrypt]

# 2. Setup MongoDB (now required for V3)
docker run -d -p 27017:27017 mongo

# 3. Add to .env
MONGO_URL=mongodb://localhost:27017
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

# 4. Restart server
python server.py
```

### V1 to V2
```bash
# 1. Install file processing libraries
pip install PyPDF2 python-docx python-multipart

# 2. Restart server
python server.py
```

### V0.9 to V1
```bash
# 1. Create .env file
cp .env.example .env

# 2. Move environment variables to .env

# 3. Update MongoDB URL if needed

# 4. Restart server
```

---

## Migration Notes

### Database Migrations

**V3.0.0:**
New collections added:
- `users` - User accounts and profiles
- `activities` - Activity tracking for gamification

**V2.0.0:**
No database changes (backward compatible)

**V1.0.0:**
No database schema changes

---

## Deprecation Notices

### Current
- None

### Future (V4.0.0)
- V1 endpoint format may be deprecated in favor of unified V3 format
- Consider migrating to V2/V3 endpoints

---

## Known Issues

### V3.0.0
- Code analysis may timeout for very large files (>5000 lines)
  - Workaround: Split into smaller files
- Leaderboard caching not implemented yet
  - May be slow with 1000+ users

### V2.0.0
- Old .doc format not supported, only .docx
  - Workaround: Convert to .docx or .pdf
- PDF extraction may fail on scanned PDFs (no OCR)
  - Workaround: Use text-based PDFs

---

## Security Updates

### V3.0.0
- Added JWT token expiration (7 days)
- Password hashing with bcrypt (cost factor 12)
- Rate limiting for auth endpoints

### V1.0.0
- Added rate limiting (60/min, 1000/hour)
- CORS protection
- Input validation on all endpoints
- Non-root Docker containers

---

## Performance Improvements

### V3.0.0
- Database indexes for user queries
- Activity logging optimized
- Code analysis caching ready

### V2.0.0
- Async file processing
- Smart document chunking
- Parallel chunk processing

### V1.0.0
- Connection pooling (50 connections)
- GZip compression
- Response caching headers

---

## Contributors

This project is maintained by the EduFlow team.

---

## Links

- **Documentation:** [README.md](README.md)
- **Installation:** [INSTALLATION.md](INSTALLATION.md)
- **API Reference:** [API_REFERENCE.md](API_REFERENCE.md)
- **Deployment:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Security:** [SECURITY.md](SECURITY.md)

---

**For detailed feature documentation, see [API_REFERENCE.md](API_REFERENCE.md)**
