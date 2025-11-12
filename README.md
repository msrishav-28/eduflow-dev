# 🎓 EduFlow - AI-Powered Education Platform

**Complete AI-powered education platform with authentication, gamification, and advanced code analysis.**

**Version:** 3.0.0 | **Status:** ✅ Production Ready | **License:** MIT

> Transform your learning experience with AI-powered tools, gamification, and intelligent code analysis.

---

## ✨ Features

### 🤖 **AI-Powered Tools**
- **Q&A System** - Get instant answers with adjustable depth
- **Smart Summarizer** - 5 styles, supports PDF/Word/Text files
- **MCQ Generator** - Difficulty levels, multiple question types  
- **Code Analyzer** - Quality scoring, error detection, line-by-line corrections

### 🔐 **Authentication & Security**
- Email/password signup and login
- JWT token-based authentication
- Secure password hashing (bcrypt)
- Rate limiting and CORS protection

### 🎮 **Gamification System**
- **Points** for every action
- **9 Badges** to unlock
- **5 Levels** (Newbie → Master)
- **Leaderboards** (monthly & all-time)
- **Streak tracking** for daily activity
- **Feature unlocks** as rewards

### 💻 **Advanced Code Analysis**
- Support for **18 programming languages**
- **Quality scoring** (0-100) with breakdown
- **5 error types**: syntax, logic, style, security, performance
- **Line-by-line corrections** with explanations
- **Performance optimization** suggestions
- **Security vulnerability** detection

### 📄 **File Upload Support**
- Drag & drop interface
- PDF, Word (DOCX), Text files
- Documents up to 50,000 characters (upgradeable)

---

## 🚀 Quick Start

```bash
# 1. Install backend dependencies
cd backend
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Add your GEMINI_API_KEY (or OPENAI/ANTHROPIC)

# 3. Start backend
python server.py

# 4. Install frontend (separate terminal)
cd frontend
npm install
npm start
```

**That's it!** Backend runs on `http://localhost:8000`, frontend on `http://localhost:3000`

### First Time Setup

1. **Create an account:** Click "Sign Up" in the header
2. **Explore features:** Try Q&A, Summarizer, MCQ Generator
3. **Earn points:** Every action gives you points and badges
4. **Check dashboard:** View your stats, badges, and leaderboard ranking
5. **Analyze code:** Upload or paste code for quality analysis (18 languages supported)

**→ For detailed setup and MongoDB configuration:** See [INSTALLATION.md](INSTALLATION.md)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[INSTALLATION.md](INSTALLATION.md)** | Complete setup guide for all versions |
| **[API_REFERENCE.md](API_REFERENCE.md)** | All API endpoints with examples |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Production deployment guide |
| **[SECURITY.md](SECURITY.md)** | Security best practices |
| **[CHANGELOG.md](CHANGELOG.md)** | Version history and updates |

---

## 🏗️ Architecture

```
EduFlow/
├── frontend/                 # React 19 application
│   ├── src/
│   │   ├── components/      # UI components
│   │   ├── hooks/           # Custom hooks
│   │   └── lib/             # Utilities
│   └── public/              # Static files
│
├── backend/                  # FastAPI server
│   ├── models/              # Data models
│   │   ├── user.py         # User & auth models
│   │   ├── activity.py     # Gamification models
│   │   └── code_analysis.py # Code analysis models
│   ├── auth.py              # Authentication service
│   ├── gamification.py      # Gamification service
│   ├── code_analyzer.py     # Code analysis service
│   ├── llm_service.py       # LLM providers
│   ├── file_processor.py    # File handling
│   ├── endpoints_v3.py      # V3 API endpoints
│   ├── endpoints.py         # V2 API endpoints
│   └── server.py            # Main application
│
├── api/                      # Vercel serverless
└── scripts/                  # Utility scripts
```

---

## 🎯 Use Cases

### For Students
- Get instant answers to questions
- Summarize textbooks and articles
- Generate practice quizzes
- Understand code with explanations
- Track learning progress with points and badges

### For Developers
- Analyze code quality
- Detect errors and security issues
- Get optimization suggestions
- Learn from line-by-line corrections

### For Educators
- Create study materials quickly
- Generate assessment questions
- Track student engagement (via gamification)
- Customize content difficulty

---

## 🛠️ Tech Stack

### Frontend
- **React 19** with modern hooks
- **Tailwind CSS** for styling
- **Radix UI** components
- **Framer Motion** animations
- **React Router** v7
- **Axios** for HTTP requests

### Backend
- **FastAPI** - Modern Python web framework
- **MongoDB** - Document database (optional for basic features)
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation
- **JWT** - Authentication tokens
- **Bcrypt** - Password hashing

### AI/LLM
- **Google Gemini** (primary)
- **OpenAI GPT** (alternative)
- **Anthropic Claude** (alternative)

### File Processing
- **PyPDF2** - PDF text extraction
- **python-docx** - Word document processing

---

## 📊 API Endpoints

### V1 (Basic AI)
- `POST /api/qa` - Question answering
- `POST /api/summarize` - Text summarization
- `POST /api/mcq` - MCQ generation
- `POST /api/explain-code` - Code explanation

### V2 (Enhanced)
- `POST /api/v2/summarize` - File upload + 5 styles
- `POST /api/v2/mcq` - Difficulty levels + question types

### V3 (Full Platform)
- `POST /api/v3/auth/signup` - User registration
- `POST /api/v3/auth/login` - User login
- `GET /api/v3/gamification/stats` - User statistics
- `GET /api/v3/gamification/leaderboard` - Rankings
- `POST /api/v3/code/analyze` - Advanced code analysis

**→ Complete API docs:** [API_REFERENCE.md](API_REFERENCE.md)

---

## 🎮 Gamification Details

### Point System
| Action | Points |
|--------|--------|
| Ask Question | +5 |
| Summarize Document | +10 |
| Generate MCQs | +15 |
| Analyze Code | +10 |
| Fix Code Errors | +20 |
| 7-Day Streak | +50 bonus |
| 30-Day Streak | +200 bonus |

### Badges
🏆 Beginner • 📚 Reader • 🎓 Scholar • 💻 Coder • 🐛 Debugger  
🔥 Streak Master • 🎯 Quiz Master • ⚡ Speed Learner • 👑 Legend

### Feature Unlocks
- **500 pts** → Upload 100K char files
- **800 pts** → 50 summary points
- **1000 pts** → 50 MCQ questions
- **2000 pts** → Upload 200K char files

---

## 🚀 Deployment

### Vercel (Recommended)
```bash
# 1. Push to GitHub
git push origin main

# 2. Deploy to Vercel
vercel --prod

# 3. Add environment variables in Vercel dashboard
# GEMINI_API_KEY, MONGO_URL, SECRET_KEY
```

### Docker
```bash
docker-compose up -d
```

### Cloud Providers
- AWS (ECS + S3 + CloudFront)
- Google Cloud (Cloud Run + Storage)
- Azure (Container Instances + Blob)

**→ Full deployment guide:** [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🔒 Security Features

- ✅ Bcrypt password hashing
- ✅ JWT token authentication
- ✅ Rate limiting (60/min, 1000/hour)
- ✅ CORS protection
- ✅ Input validation
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ Security headers (Nginx)
- ✅ Non-root Docker containers

**→ Security details:** [SECURITY.md](SECURITY.md)

---

## 📈 Roadmap

### V3.0 (Current) ✅
- ✅ Authentication system (JWT, bcrypt)
- ✅ Gamification (points, badges, levels, leaderboards)
- ✅ Advanced code analyzer (18 languages)
- ✅ File upload (drag & drop)
- ✅ Dark mode UI
- ✅ Responsive design

### V4.0 (Planned)
- [ ] Social features (share summaries, collaborate)
- [ ] Team competitions and challenges
- [ ] Email notifications
- [ ] Profile customization
- [ ] More badges and achievements
- [ ] Custom challenges
- [ ] Mobile app

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React team for the amazing frontend library
- MongoDB for flexible data storage
- Google, OpenAI, Anthropic for LLM APIs
- All open-source contributors

---

## 📞 Support

- **Documentation:** Complete guides in `/docs`
- **Issues:** GitHub Issues
- **Security:** See [SECURITY.md](SECURITY.md)
- **Email:** support@eduflow.example.com

---

## 🌟 Star History

If you find this project helpful, please consider giving it a ⭐!

---

## 📊 Project Stats

- **Lines of Code:** 5,000+
- **Components:** 12 React components
- **API Endpoints:** 15+ (V1, V2, V3)
- **Supported Languages:** 18
- **Documentation:** 5 comprehensive guides
- **Badges:** 9 unlockable achievements
- **Levels:** 5 progression tiers

---

## 🔧 Troubleshooting

### Frontend not showing new UI?
```bash
# Hard refresh browser
Ctrl + Shift + R (Windows/Linux)
Cmd + Shift + R (Mac)

# Or clear cache and restart
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Backend errors?
```bash
# Check Python version (3.8+ required)
python --version

# Reinstall dependencies
pip install -r backend/requirements.txt

# Check environment variables
cat backend/.env  # Must have API keys
```

### MongoDB connection issues?
```bash
# MongoDB is optional for V1/V2
# Required for V3 authentication
# Check MONGODB_URI in .env
# Or use without auth: comment out MongoDB requirements
```

**→ More help:** [INSTALLATION.md](INSTALLATION.md) or open an issue

---

**Built with ❤️ for education**

**Get started:** [INSTALLATION.md](INSTALLATION.md) | **API Docs:** [API_REFERENCE.md](API_REFERENCE.md) | **Deploy:** [DEPLOYMENT.md](DEPLOYMENT.md)
