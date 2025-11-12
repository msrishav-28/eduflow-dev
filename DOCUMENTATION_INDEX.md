# 📚 Documentation Index

Complete guide to all EduFlow documentation.

---

## 🚀 Quick Start

**New users start here:**

1. **[INSTALLATION.md](INSTALLATION.md)** - Complete setup guide (5 minutes)
2. **[API_REFERENCE.md](API_REFERENCE.md)** - All API endpoints  
3. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deploy to production

---

## 📖 Main Documentation

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[README.md](README.md)** | Project overview & features | Start here |
| **[INSTALLATION.md](INSTALLATION.md)** | Setup instructions | Before running |
| **[API_REFERENCE.md](API_REFERENCE.md)** | Complete API docs | When building |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Production deployment | Before launch |
| **[SECURITY.md](SECURITY.md)** | Security best practices | For production |
| **[CHANGELOG.md](CHANGELOG.md)** | Version history | When upgrading |

---

## 🎯 By Use Case

### I want to...

#### **Get started quickly**
→ Read [INSTALLATION.md](INSTALLATION.md) Quick Start section (5 minutes)

#### **Build with the API**
→ Read [API_REFERENCE.md](API_REFERENCE.md) for all endpoints

#### **Deploy to production**
→ Follow [DEPLOYMENT.md](DEPLOYMENT.md) for your platform

#### **Add authentication to my app**
→ See [API_REFERENCE.md - V3 Endpoints](API_REFERENCE.md#v3-endpoints-full-platform)

#### **Use file upload features**
→ See [API_REFERENCE.md - V2 Endpoints](API_REFERENCE.md#v2-endpoints-enhanced-features)

#### **Understand what changed**
→ Read [CHANGELOG.md](CHANGELOG.md)

#### **Report a security issue**
→ Follow [SECURITY.md](SECURITY.md)

---

## 🏗️ Architecture Overview

```
EduFlow/
├── frontend/          # React 19 app
│   ├── src/          # Source code
│   └── public/       # Static files
│
├── backend/          # FastAPI server
│   ├── models/       # Data models
│   ├── auth.py       # Authentication
│   ├── gamification.py  # Points & badges
│   ├── code_analyzer.py # Code analysis
│   ├── endpoints_v3.py  # V3 endpoints
│   └── server.py     # Main server
│
├── api/              # Vercel serverless
└── scripts/          # Utility scripts
```

---

## ✨ Feature Versions

### V3 (Current) - Full Platform
- ✅ Authentication (email/password, JWT)
- ✅ Gamification (points, badges, leaderboards)
- ✅ Advanced code analyzer (18 languages, quality scoring)
- ✅ Line-by-line code corrections
- ✅ Performance & security tips

### V2 - Enhanced Features
- ✅ File upload (PDF, Word, Text)
- ✅ 5 summary styles
- ✅ Difficulty-based MCQs
- ✅ Large document support (50K+ chars)

### V1 - Core AI
- ✅ Q&A system
- ✅ Text summarizer
- ✅ MCQ generator
- ✅ Code explainer

---

## 🔧 Tech Stack

### Frontend
- React 19, Tailwind CSS, Radix UI
- Framer Motion, Lucide Icons
- React Router, Axios

### Backend
- FastAPI, Uvicorn
- MongoDB (Motor async)
- PyJWT, Passlib (auth)
- PyPDF2, python-docx (files)

### LLM Providers
- Google Gemini (primary)
- OpenAI GPT
- Anthropic Claude

---

## 📝 Quick Examples

### Basic Q&A
```javascript
const response = await fetch('/api/qa', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    question: 'What is AI?',
    depth: 'balanced'
  })
});
```

### File Upload
```javascript
const formData = new FormData();
formData.append('file', file);
formData.append('style', 'long_notes');

const response = await fetch('/api/v2/summarize', {
  method: 'POST',
  body: formData
});
```

### Authentication
```javascript
const {access_token} = await fetch('/api/v3/auth/signup', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePass123'
  })
}).then(r => r.json());

// Use token for protected endpoints
fetch('/api/v3/code/analyze', {
  headers: {'Authorization': `Bearer ${access_token}`},
  ...
});
```

---

## 🎮 Gamification Overview

### Points
- Q&A: +5 points
- Summarize: +10 points
- MCQ: +15 points
- Code analysis: +10 points
- 7-day streak: +50 bonus

### Levels
1. Newbie (0-100 pts)
2. Learner (101-500)
3. Scholar (501-1K)
4. Expert (1K-5K)
5. Master (5K+)

### Feature Unlocks
- 500 pts → 100K char files
- 1000 pts → 50 MCQs
- 2000 pts → 200K char files

---

## 🚀 Deployment Quick Links

| Platform | Guide Link | Difficulty |
|----------|------------|------------|
| Vercel | [DEPLOYMENT.md#vercel](DEPLOYMENT.md#vercel-deployment-recommended) | ⭐ Easy |
| Docker | [DEPLOYMENT.md#docker](DEPLOYMENT.md#docker-deployment) | ⭐⭐ Medium |
| AWS | [DEPLOYMENT.md#aws](DEPLOYMENT.md#aws-deployment) | ⭐⭐⭐ Advanced |
| GCP | [DEPLOYMENT.md#gcp](DEPLOYMENT.md#google-cloud-platform) | ⭐⭐⭐ Advanced |

---

## 🐛 Troubleshooting

Common issues and solutions:

| Issue | Solution | Doc Link |
|-------|----------|----------|
| "No LLM API key" | Add GEMINI_API_KEY to .env | [INSTALLATION.md](INSTALLATION.md) |
| "MongoDB connection failed" | Check MONGO_URL or disable | [INSTALLATION.md](INSTALLATION.md#mongodb-setup-optionalrequired) |
| "Module not found" | Run `pip install -r requirements.txt` | [INSTALLATION.md](INSTALLATION.md) |
| Frontend can't reach backend | Check CORS_ORIGINS | [DEPLOYMENT.md](DEPLOYMENT.md) |

---

## 📞 Support & Contributing

- **Issues:** GitHub Issues
- **Security:** See [SECURITY.md](SECURITY.md)
- **Contributing:** Pull requests welcome!
- **License:** MIT

---

## 📈 Latest Updates

See [CHANGELOG.md](CHANGELOG.md) for version history.

**Latest:** V3.0.0 (December 2024)
- Authentication system
- Gamification (points, badges, leaderboards)
- Advanced code analyzer with quality scoring
- 18 programming languages supported

---

## ⚡ Quick Command Reference

```bash
# Install
cd backend && pip install -r requirements.txt
cd frontend && npm install

# Run development
cd backend && python server.py
cd frontend && npm start

# Run with Docker
docker-compose up -d

# Deploy to Vercel
vercel --prod
```

---

**Choose your documentation path:**
- 🆕 New user? → [INSTALLATION.md](INSTALLATION.md)
- 💻 Building with API? → [API_REFERENCE.md](API_REFERENCE.md)
- 🚀 Deploying? → [DEPLOYMENT.md](DEPLOYMENT.md)
- 🔒 Security concerns? → [SECURITY.md](SECURITY.md)

---

**All documentation consolidated and up to date!** 📚
