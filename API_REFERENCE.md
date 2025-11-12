# API Reference

Complete API documentation for all EduFlow endpoints (V1, V2, V3).

---

## Base URL

- **Development:** `http://localhost:8000`
- **Production:** `https://your-app.vercel.app`

---

## Authentication

V3 endpoints require Bearer token authentication:

```http
Authorization: Bearer <your-jwt-token>
```

Get token from `/api/v3/auth/signup` or `/api/v3/auth/login`

---

## V1 Endpoints (Basic AI Features)

### Health & Status

#### GET `/health`
Basic health check

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00"
}
```

#### GET `/readiness`
Readiness check with database status

**Response:**
```json
{
  "status": "ready",
  "database": "connected",
  "llm_provider": "gemini",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Q&A System

#### POST `/api/qa`
Generate AI-powered answers

**Request:**
```json
{
  "question": "What is machine learning?",
  "depth": "balanced"
}
```

**Parameters:**
- `question` (string, required): 1-1000 chars
- `depth` (string, optional): "concise", "balanced", "detailed"

**Response:**
```json
{
  "id": "uuid",
  "question": "What is machine learning?",
  "answer": "Machine learning is...",
  "depth": "balanced",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Summarizer

#### POST `/api/summarize`
Summarize text into bullet points

**Request:**
```json
{
  "text": "Long text to summarize...",
  "max_points": 5
}
```

**Parameters:**
- `text` (string, required): 10-10000 chars
- `max_points` (integer, optional): 3-10, default 5

**Response:**
```json
{
  "id": "uuid",
  "original_text": "Long text...",
  "summary": ["Point 1", "Point 2", "Point 3"],
  "timestamp": "2024-01-15T10:30:00"
}
```

### MCQ Generator

#### POST `/api/mcq`
Generate multiple choice questions

**Request:**
```json
{
  "topic": "Physics",
  "num_questions": 5
}
```

**Parameters:**
- `topic` (string, required): 1-200 chars
- `num_questions` (integer, optional): 1-10, default 5

**Response:**
```json
{
  "id": "uuid",
  "topic": "Physics",
  "questions": [
    {
      "question": "What is force?",
      "options": [
        {"letter": "A", "text": "Option A"},
        {"letter": "B", "text": "Option B"},
        {"letter": "C", "text": "Option C"},
        {"letter": "D", "text": "Option D"}
      ],
      "correct_answer": "A",
      "explanation": "Explanation here"
    }
  ],
  "timestamp": "2024-01-15T10:30:00"
}
```

### Code Explainer

#### POST `/api/explain-code`
Explain code snippets

**Request:**
```json
{
  "code": "def hello():\n    print('Hello')",
  "language": "python"
}
```

**Parameters:**
- `code` (string, required): 1-5000 chars
- `language` (string, required): programming language

**Response:**
```json
{
  "id": "uuid",
  "code": "def hello()...",
  "language": "python",
  "explanation": "This code defines...",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## V2 Endpoints (Enhanced Features)

### Advanced Summarizer

#### POST `/api/v2/summarize`
File upload + multiple summary styles

**Request:** multipart/form-data
- `file` (file, optional): PDF, DOCX, or TXT file
- `text` (string, optional): Direct text input
- `style` (string, optional): "short_notes", "long_notes", "balanced", "bullet_points", "detailed"
- `max_points` (integer, optional): 1-20, default 5

**One of file or text required**

**Response:**
```json
{
  "id": "uuid",
  "original_length": 5230,
  "summary": ["Point 1", "Point 2", "Point 3"],
  "style": "long_notes",
  "timestamp": "2024-01-15T10:30:00",
  "source": "file (pdf)"
}
```

#### POST `/api/v2/summarize/text`
Quick text-only summarizer

**Request:**
```json
{
  "text": "Text to summarize...",
  "style": "short_notes",
  "max_points": 5
}
```

### Advanced MCQ Generator

#### POST `/api/v2/mcq`
File upload + difficulty levels + question types

**Request:** multipart/form-data
- `file` (file, optional): PDF, DOCX, or TXT
- `text` (string, optional): Direct text
- `num_questions` (integer, optional): 1-20, default 5
- `difficulty` (string, optional): "easy", "medium", "hard"
- `question_type` (string, optional): "factual", "conceptual", "application", "mixed"

**Response:**
```json
{
  "id": "uuid",
  "source_length": 3200,
  "questions": [...],
  "difficulty": "hard",
  "question_type": "conceptual",
  "timestamp": "2024-01-15T10:30:00",
  "source": "file (pdf)"
}
```

#### POST `/api/v2/mcq/text`
Quick text-only MCQ generator

**Request:**
```json
{
  "text": "Content...",
  "num_questions": 5,
  "difficulty": "medium",
  "question_type": "mixed"
}
```

---

## V3 Endpoints (Full Platform)

### Authentication

#### POST `/api/v3/auth/signup`
Register new user

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "display_name": "John Doe"
}
```

**Password requirements:**
- Min 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 digit

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "display_name": "John Doe",
    "points": 0,
    "level": 1,
    "badges": [],
    "streak_days": 0,
    "created_at": "2024-01-15T10:30:00",
    "total_activities": 0,
    "max_file_size": 50000,
    "max_mcq_questions": 20,
    "max_summary_points": 20
  }
}
```

#### POST `/api/v3/auth/login`
Login existing user

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response:** Same as signup

#### GET `/api/v3/auth/me`
Get current user info

**Headers:** `Authorization: Bearer <token>`

**Response:** User object

### Gamification

#### GET `/api/v3/gamification/stats`
Get user statistics and progress

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "points": 1250,
  "level": 3,
  "level_name": "Scholar",
  "points_to_next_level": 250,
  "badges": [
    {
      "id": "beginner",
      "name": "🏆 Beginner",
      "description": "Complete your first activity"
    }
  ],
  "streak_days": 7,
  "total_activities": 45,
  "activities_breakdown": {
    "qa": 10,
    "summarize": 15,
    "mcq": 10,
    "code_explain": 8,
    "code_fix": 2
  },
  "feature_unlocks": {
    "max_file_size": 100000,
    "max_mcq_questions": 50,
    "max_summary_points": 20
  },
  "rank": 42
}
```

#### GET `/api/v3/gamification/leaderboard`
Get leaderboard rankings

**Query Parameters:**
- `period` (string, optional): "monthly" or "all_time", default "monthly"
- `limit` (integer, optional): 1-100, default 10

**Response:**
```json
{
  "period": "monthly",
  "leaderboard": [
    {
      "rank": 1,
      "user_id": "...",
      "display_name": "Top Player",
      "points": 5420,
      "level": 5
    }
  ]
}
```

### Advanced Code Analysis

#### POST `/api/v3/code/analyze`
Comprehensive code analysis with file upload

**Headers:** `Authorization: Bearer <token>` (optional)

**Request:** multipart/form-data
- `file` (file, optional): Code file
- `code` (string, optional): Direct code input
- `language` (string, required): Programming language

**Supported Languages:**
Python, JavaScript, TypeScript, Java, C++, C, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, Scala, R, SQL, HTML, CSS

**Response:**
```json
{
  "id": "uuid",
  "user_id": "user-id-if-authenticated",
  "language": "python",
  "has_errors": true,
  "error_count": 3,
  "errors": [
    {
      "type": "syntax_error",
      "line": 15,
      "column": 10,
      "message": "Missing closing parenthesis",
      "severity": "high",
      "suggestion": "Add ) at end of line"
    }
  ],
  "quality_score": 72,
  "score_breakdown": {
    "syntax": 16,
    "logic": 18,
    "style": 14,
    "security": 20,
    "performance": 14
  },
  "line_corrections": [
    {
      "line": 15,
      "original": "print('Hello'",
      "corrected": "print('Hello')",
      "reason": "Missing closing parenthesis"
    }
  ],
  "corrected_code": "# Full corrected version...",
  "explanation": "Your code has a few issues...",
  "suggestions": [
    "Use meaningful variable names",
    "Add docstrings to functions"
  ],
  "performance_tips": [
    "Use list comprehension instead of loop",
    "Cache repeated calculations"
  ],
  "security_issues": [
    "Avoid eval() with user input"
  ],
  "timestamp": "2024-01-15T10:30:00"
}
```

**Error Types:**
- `syntax_error` - Code won't run
- `logic_error` - Code runs but wrong logic
- `style` - Code style issues
- `security` - Security vulnerabilities
- `performance` - Performance problems

**Severity Levels:**
- `high` - Must fix
- `medium` - Should fix
- `low` - Nice to fix

#### POST `/api/v3/code/quick-check`
Quick error check (faster, simpler)

**Headers:** `Authorization: Bearer <token>` (optional)

**Request:**
```json
{
  "code": "def hello():\n    print('test'",
  "language": "python"
}
```

**Response:**
```json
{
  "has_errors": true,
  "error_count": 1,
  "errors": ["Missing closing parenthesis on line 2"]
}
```

---

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 401 | Unauthorized (missing/invalid token) |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 429 | Too Many Requests (rate limited) |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

---

## Rate Limiting

**Default Limits:**
- 60 requests per minute
- 1000 requests per hour

**Headers:**
- `X-RateLimit-Remaining-Minute`
- `X-RateLimit-Remaining-Hour`

**Response when limited:**
```json
{
  "detail": "Rate limit exceeded. Try again in X seconds."
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

**Validation errors (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "type": "value_error"
    }
  ]
}
```

---

## Gamification Points

| Action | Points Earned |
|--------|---------------|
| Q&A | +5 |
| Summarize | +10 |
| Generate MCQs | +15 |
| Explain Code | +10 |
| Fix Code Errors | +20 |
| Upload File | +5 (first of session) |
| Daily Login | +10 (first activity) |
| 7-Day Streak | +50 (bonus) |
| 30-Day Streak | +200 (bonus) |

---

## Feature Unlocks

Earn points to unlock enhanced features:

| Points | Unlock |
|--------|--------|
| 500 | Upload files up to 100K chars |
| 800 | Generate up to 50 summary points |
| 1000 | Generate up to 50 MCQ questions |
| 2000 | Upload files up to 200K chars |

---

## Examples

### Complete User Flow

```javascript
// 1. Sign up
const signup = await fetch('/api/v3/auth/signup', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePass123',
    display_name: 'John Doe'
  })
});
const {access_token, user} = await signup.json();

// 2. Analyze code (earn 10 points!)
const formData = new FormData();
formData.append('code', 'def hello():\n    print("hi")');
formData.append('language', 'python');

const analysis = await fetch('/api/v3/code/analyze', {
  method: 'POST',
  headers: {'Authorization': `Bearer ${access_token}`},
  body: formData
});
const result = await analysis.json();

// 3. Check stats
const stats = await fetch('/api/v3/gamification/stats', {
  headers: {'Authorization': `Bearer ${access_token}`}
});
const userStats = await stats.json();
console.log('Points:', userStats.points);
console.log('Level:', userStats.level);
```

### File Upload

```javascript
// Upload PDF and summarize
const fileInput = document.getElementById('file');
const file = fileInput.files[0];

const formData = new FormData();
formData.append('file', file);
formData.append('style', 'long_notes');
formData.append('max_points', 10);

const response = await fetch('/api/v2/summarize', {
  method: 'POST',
  body: formData
});
const summary = await response.json();
```

---

## SDKs & Libraries

### Python

```python
import requests

# Q&A
response = requests.post('http://localhost:8000/api/qa', json={
    'question': 'What is AI?',
    'depth': 'balanced'
})
answer = response.json()

# With authentication
headers = {'Authorization': f'Bearer {token}'}
response = requests.post('http://localhost:8000/api/v3/code/analyze',
    headers=headers,
    files={'file': open('code.py', 'rb')},
    data={'language': 'python'}
)
analysis = response.json()
```

### JavaScript/TypeScript

```typescript
// Using fetch
const response = await fetch('/api/qa', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    question: 'What is AI?',
    depth: 'balanced'
  })
});
const answer = await response.json();

// Using axios
import axios from 'axios';

const answer = await axios.post('/api/qa', {
  question: 'What is AI?',
  depth: 'balanced'
});
```

---

## OpenAPI / Swagger

Interactive API documentation available at:
- **Development:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

(Only available in development mode when `DEBUG=True`)

---

**For deployment guides, see [DEPLOYMENT.md](DEPLOYMENT.md)**
