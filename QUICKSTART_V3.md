# Quick Start Guide - V3 Complete System

Get EduFlow running with all V3 features in under 5 minutes.

---

## 🚀 Start in 3 Steps

### Step 1: Start Backend (Terminal 1)

```bash
cd backend

# Install dependencies (if not done)
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Add your API keys to .env
# Required: GEMINI_API_KEY=your-key
# Optional for V3: MONGO_URL=mongodb://localhost:27017
# Required for V3: SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

# Start server
python server.py
```

**✅ Backend Ready:** `http://localhost:8000`

---

### Step 2: Start Frontend (Terminal 2)

```bash
cd frontend

# Install dependencies (if not done)
npm install

# Start development server
npm start
```

**✅ Frontend Ready:** `http://localhost:3000`

---

### Step 3: Test the System

1. **Open Browser:** `http://localhost:3000`
2. **Click "Sign Up"** in the header
3. **Create Account:**
   - Email: `test@example.com`
   - Password: `TestPass123` (must have uppercase, lowercase, digit)
   - Display Name: `Test User`
4. **Explore:**
   - Dashboard → See your stats
   - Code Analyzer → Upload code
   - Try existing tools → Earn points!

---

## 🎯 What You Can Do Now

### Without Login
- ✅ Use Q&A system
- ✅ Summarize text
- ✅ Generate MCQs
- ✅ Basic code explainer

### With Login (V3 Features)
- ✅ **Advanced Code Analyzer** (18 languages, quality scoring)
- ✅ **Gamification** (points, badges, levels)
- ✅ **Dashboard** (track your progress)
- ✅ **Leaderboard** (compete with others)
- ✅ **Profile** (view your stats)

---

## 📊 Test Checklist

```bash
# ✅ Backend health check
curl http://localhost:8000/health

# ✅ Create account
# Use signup form in browser

# ✅ Login
# Use login form in browser

# ✅ View dashboard
# Navigate to /dashboard after login

# ✅ Analyze code
# Navigate to /code-analyzer, upload a file

# ✅ Check leaderboard
# Go to Dashboard > Leaderboard tab
```

---

## 🎮 Quick Feature Tour

### 1. Sign Up & Login
```
Navigate to: http://localhost:3000
Click: "Sign Up" button in header
Fill form → Create account
Redirected to: /dashboard
```

### 2. Dashboard Overview
```
Location: /dashboard
See:
  - Points, Level, Badges, Streak (cards)
  - Activity breakdown (chart)
  - Feature unlocks (limits)
Tabs:
  - Overview: Your stats
  - Badges: Collect 9 badges
  - Leaderboard: Monthly rankings
```

### 3. Code Analyzer
```
Location: /code-analyzer
Steps:
  1. Select language (18 options)
  2. Upload file OR paste code
  3. Click "Analyze Code"
  4. View:
     - Quality score (0-100)
     - Errors (syntax, logic, style, security, performance)
     - Line-by-line corrections
     - Performance tips
     - Security warnings
     - Corrected code
```

### 4. Earn Points
```
Do any action:
  - Ask question: +5 pts
  - Summarize: +10 pts
  - Generate MCQ: +15 pts
  - Analyze code: +10 pts
  - Fix code: +20 pts

Watch:
  - Points increase in header avatar
  - Level up when reaching threshold
  - Badges unlock automatically
  - Rank changes on leaderboard
```

---

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```bash
# Required
GEMINI_API_KEY=your-gemini-key

# V3 Features (Optional)
MONGO_URL=mongodb://localhost:27017
SECRET_KEY=your-32-char-secret-key

# Optional
ENV=development
DEBUG=True
```

**Frontend (.env):**
```bash
# Only needed if backend is not on localhost:8000
REACT_APP_BACKEND_URL=http://localhost:8000
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Install dependencies again
pip install -r requirements.txt

# Check if port 8000 is free
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Mac/Linux
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 18+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check if port 3000 is free
netstat -ano | findstr :3000  # Windows
lsof -i :3000                 # Mac/Linux
```

### MongoDB connection error
```bash
# V3 features require MongoDB
# Option 1: Install locally
# Option 2: Use Docker
docker run -d -p 27017:27017 mongo

# Option 3: Use MongoDB Atlas (free)
# Get connection string from https://mongodb.com/atlas
```

### "Network Error" in frontend
```bash
# Check backend is running
curl http://localhost:8000/health

# Check CORS (should be enabled by default)
# Verify API_BASE_URL in frontend matches backend port
```

---

## 📈 What's New in V3

| Feature | Status | Location |
|---------|--------|----------|
| Authentication | ✅ | /login, /signup |
| Gamification | ✅ | /dashboard |
| Code Analyzer | ✅ | /code-analyzer |
| Leaderboard | ✅ | /dashboard (Leaderboard tab) |
| User Profile | ✅ | /profile |
| Points System | ✅ | All activities |
| Badges | ✅ | /dashboard (Badges tab) |
| Levels | ✅ | 5 levels (Newbie → Master) |
| Feature Unlocks | ✅ | Based on points |

---

## 🎊 Success Indicators

You'll know everything is working when:

- ✅ Backend shows: `V3 endpoints loaded`
- ✅ Frontend loads without errors
- ✅ Can create account and login
- ✅ Dashboard shows your stats
- ✅ Header shows user avatar (not sign in button)
- ✅ Code analyzer returns results
- ✅ Points increase after activities
- ✅ Leaderboard shows rankings

---

## 📚 Next Steps

1. **Read Full Docs:**
   - [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md) - Frontend details
   - [API_REFERENCE.md](API_REFERENCE.md) - API endpoints
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Deploy to production

2. **Customize:**
   - Add more badges
   - Change point values
   - Modify UI theme colors
   - Add more languages

3. **Deploy:**
   - Follow [DEPLOYMENT.md](DEPLOYMENT.md)
   - Use Vercel for easy deployment
   - Configure MongoDB Atlas

---

## ⚡ Common Commands

```bash
# Backend
cd backend
python server.py                    # Start server
pip install -r requirements.txt     # Install deps

# Frontend
cd frontend
npm start                           # Start dev server
npm run build                       # Build for production
npm install                         # Install deps

# MongoDB (Docker)
docker run -d -p 27017:27017 mongo  # Start MongoDB
docker ps                           # Check running containers

# Testing
curl http://localhost:8000/health   # Backend health
curl http://localhost:8000/api/     # API root
```

---

## 🎯 Quick Test Script

```bash
# Run this to test everything works

# 1. Backend health
curl http://localhost:8000/health
# Expected: {"status": "ok", ...}

# 2. Signup (replace with your info)
curl -X POST http://localhost:8000/api/v3/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123","display_name":"Test User"}'
# Expected: {"access_token": "...", "user": {...}}

# 3. Save the token from response, then check stats
curl http://localhost:8000/api/v3/gamification/stats \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
# Expected: {"points": 0, "level": 1, ...}
```

---

## 💡 Pro Tips

1. **Use MongoDB for full features**
   - Basic AI works without MongoDB
   - V3 auth/gamification requires MongoDB

2. **Generate secure secret key**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Check logs for errors**
   - Backend: Terminal output
   - Frontend: Browser console (F12)

4. **Multiple LLM providers**
   - Gemini (recommended, free tier)
   - OpenAI (paid)
   - Anthropic (paid)
   - Backend auto-selects available provider

5. **Dark mode**
   - Click sun/moon icon in header
   - Persists in localStorage
   - All components support both themes

---

## 🆘 Get Help

- **Documentation:** All .md files in project root
- **Issues:** Check browser console and backend logs
- **API Docs:** `http://localhost:8000/docs` (when DEBUG=True)

---

**You're all set!** Enjoy your complete AI-powered education platform! 🚀

Start with: `python server.py` (backend) and `npm start` (frontend)
