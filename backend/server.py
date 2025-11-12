from fastapi import FastAPI, APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import openai
import json
import google.generativeai as genai
import time
import asyncio
from rate_limiter import RateLimitMiddleware


# Configure logging FIRST before any other operations
logging.basicConfig(
    level=logging.INFO if os.getenv('ENV', 'development') != 'production' else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Environment configuration
ENV = os.getenv('ENV', 'development')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
IS_PRODUCTION = ENV == 'production'

# MongoDB connection with error handling (optional)
client = None
db = None
mongodb_available = False

try:
    mongo_url = os.environ.get('MONGO_URL')
    if mongo_url and mongo_url != 'none':
        client = AsyncIOMotorClient(
            mongo_url,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            retryWrites=True,
            maxPoolSize=50
        )
        db_name = os.environ.get('DB_NAME', 'eduflow')
        db = client[db_name]
        mongodb_available = True
        logger.info(f"MongoDB configured for database: {db_name}")
    else:
        logger.warning("MongoDB not configured - running without database persistence")
except Exception as e:
    logger.warning(f"MongoDB connection failed: {str(e)} - continuing without database")
    client = None
    db = None
    mongodb_available = False

# Configure LLM Providers
openai_api_key = os.environ.get('OPENAI_API_KEY')
gemini_api_key = os.environ.get('GEMINI_API_KEY')
anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY')

if openai_api_key:
    openai.api_key = openai_api_key

if gemini_api_key:
    genai.configure(api_key=gemini_api_key)

# Determine which LLM provider to use (with automatic fallback)
def get_available_llm_provider():
    """Returns the available LLM provider in order of preference"""
    if gemini_api_key:
        return "gemini"
    elif openai_api_key:
        return "openai"
    elif anthropic_api_key:
        return "anthropic"
    else:
        return None

DEFAULT_LLM_PROVIDER = get_available_llm_provider()

# Create the main app with production configurations
app = FastAPI(
    title="EduFlow API",
    description="AI-powered education platform API",
    version="1.0.0",
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
    openapi_url="/openapi.json" if DEBUG else None
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Request ID Middleware for tracking
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Add request ID to logging context
    old_factory = logging.getLogRecordFactory()
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.request_id = request_id
        return record
    logging.setLogRecordFactory(record_factory)
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    logging.setLogRecordFactory(old_factory)
    return response

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, 'request_id', 'unknown')
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error" if IS_PRODUCTION else str(exc),
            "request_id": request_id
        }
    )


# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class QARequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    depth: str = Field(default="balanced", description="concise, balanced, or detailed")
    
    @validator('question')
    def validate_question(cls, v):
        if not v or not v.strip():
            raise ValueError('Question cannot be empty')
        return v.strip()
    
    @validator('depth')
    def validate_depth(cls, v):
        if v not in ['concise', 'balanced', 'detailed']:
            raise ValueError('Depth must be one of: concise, balanced, detailed')
        return v

class QAResponse(BaseModel):
    id: str
    question: str
    answer: str
    depth: str
    timestamp: datetime

class SummarizerRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=10000)
    max_points: int = Field(default=5, ge=1, le=20, description="Maximum number of bullet points")
    
    @validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        return v.strip()

class SummarizerResponse(BaseModel):
    id: str
    original_text: str
    summary: List[str]
    timestamp: datetime

class MCQRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200)
    num_questions: int = Field(default=5, ge=1, le=20)
    
    @validator('topic')
    def validate_topic(cls, v):
        if not v or not v.strip():
            raise ValueError('Topic cannot be empty')
        return v.strip()

class MCQOption(BaseModel):
    letter: str
    text: str

class MCQuestion(BaseModel):
    question: str
    options: List[MCQOption]
    correct_answer: str
    explanation: str

class MCQResponse(BaseModel):
    id: str
    topic: str
    questions: List[MCQuestion]
    timestamp: datetime

class CodeExplainerRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=5000)
    language: str = Field(default="python")
    
    @validator('code')
    def validate_code(cls, v):
        if not v or not v.strip():
            raise ValueError('Code cannot be empty')
        return v.strip()
    
    @validator('language')
    def validate_language(cls, v):
        allowed_languages = ['python', 'javascript', 'java', 'cpp', 'csharp', 'go', 'rust', 'typescript']
        if v.lower() not in allowed_languages:
            raise ValueError(f'Language must be one of: {", ".join(allowed_languages)}')
        return v.lower()

class CodeExplainerResponse(BaseModel):
    id: str
    code: str
    language: str
    explanation: str
    timestamp: datetime


# Database Helper function
async def save_to_db(collection_name: str, data: dict) -> bool:
    """Save data to database if available, otherwise just log"""
    if mongodb_available and db:
        try:
            await db[collection_name].insert_one(data)
            return True
        except Exception as e:
            logger.warning(f"Failed to save to database: {str(e)}")
    else:
        logger.debug(f"Database not available - skipping save to {collection_name}")
    return False

# LLM Helper functions
async def call_llm(prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
    """Call LLM with automatic provider selection and fallback"""
    provider = DEFAULT_LLM_PROVIDER
    
    if not provider:
        raise HTTPException(
            status_code=500, 
            detail="No LLM API key configured. Please set GEMINI_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY"
        )
    
    try:
        if provider == "gemini":
            return await call_gemini(prompt, temperature, max_tokens)
        elif provider == "openai":
            return await call_openai(prompt, temperature, max_tokens)
        elif provider == "anthropic":
            return await call_anthropic(prompt, temperature, max_tokens)
    except Exception as e:
        logger.error(f"LLM error with {provider}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")


async def call_gemini(prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
    """Call Google Gemini 2.5 Flash API"""
    if not gemini_api_key:
        raise Exception("Gemini API key not configured")
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
        )
        return response.text.strip()
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        raise


async def call_openai(prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
    """Call OpenAI API with error handling"""
    if not openai_api_key:
        raise Exception("OpenAI API key not configured")
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise


async def call_anthropic(prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
    """Call Anthropic Claude API with error handling"""
    if not anthropic_api_key:
        raise Exception("Anthropic API key not configured")
    
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=anthropic_api_key)
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except Exception as e:
        logger.error(f"Anthropic API error: {str(e)}")
        raise


# Health check endpoints (outside /api prefix for load balancers)
@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/readiness")
async def readiness_check():
    """Readiness check - validates database connectivity"""
    try:
        # Check MongoDB connection if available
        db_status = "not_configured"
        if mongodb_available and client:
            try:
                await client.admin.command('ping')
                db_status = "connected"
            except Exception as db_error:
                logger.warning(f"Database ping failed: {str(db_error)}")
                db_status = "unavailable"
        
        # Check LLM provider
        llm_status = DEFAULT_LLM_PROVIDER or "not_configured"
        
        # App is ready if LLM is configured (database is optional)
        is_ready = DEFAULT_LLM_PROVIDER is not None
        
        return {
            "status": "ready" if is_ready else "degraded",
            "database": db_status,
            "llm_provider": llm_status,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,  # Return 200 even if degraded
            content={
                "status": "degraded",
                "database": "unavailable",
                "error": str(e) if DEBUG else "Service degraded",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {
        "message": "EduFlow API",
        "version": "1.0.0",
        "status": "operational",
        "llm_provider": DEFAULT_LLM_PROVIDER or "not_configured",
        "endpoints": {
            "qa": "POST /api/qa - Ask questions and get AI answers",
            "summarizer": "POST /api/summarize - Summarize text passages",
            "mcq": "POST /api/mcq - Generate multiple choice questions",
            "code_explainer": "POST /api/explain-code - Explain code snippets"
        }
    }

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    await save_to_db('status_checks', status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    if not mongodb_available or not db:
        return []
    try:
        status_checks = await db.status_checks.find().to_list(1000)
        return [StatusCheck(**status_check) for status_check in status_checks]
    except Exception as e:
        logger.warning(f"Failed to fetch status checks: {str(e)}")
        return []

@api_router.post("/qa", response_model=QAResponse)
async def qa_endpoint(request: QARequest):
    """Generate AI-powered answers to questions"""
    try:
        depth_instructions = {
            "concise": "Provide a short, concise answer (1-2 sentences)",
            "balanced": "Provide a balanced answer with key details (3-4 sentences)",
            "detailed": "Provide a detailed, comprehensive answer with examples (5-7 sentences)"
        }
        
        prompt = f"""Answer the following question with clarity and accuracy.
        
Depth level: {request.depth} - {depth_instructions.get(request.depth, 'balanced')}

Question: {request.question}

Provide a clear, structured answer:"""
        
        answer = await call_llm(prompt, max_tokens=1500)
        
        response_obj = QAResponse(
            id=str(uuid.uuid4()),
            question=request.question,
            answer=answer,
            depth=request.depth,
            timestamp=datetime.utcnow()
        )
        
        # Store in DB (optional)
        await save_to_db('qa_responses', response_obj.dict(by_alias=False, exclude_unset=True))
        
        return response_obj
    except Exception as e:
        logger.error(f"QA endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/summarize", response_model=SummarizerResponse)
async def summarizer_endpoint(request: SummarizerRequest):
    """Summarize text into key bullet points"""
    try:
        prompt = f"""Summarize the following text into {request.max_points} key bullet points. 
Keep each point concise and clear. Focus on the most important information.

Text:
{request.text}

Provide the summary as a numbered list of bullet points:"""
        
        response_text = await call_llm(prompt, max_tokens=1000)
        
        # Parse bullet points
        lines = response_text.split('\n')
        bullets = [line.strip().lstrip('0123456789.-) ') for line in lines if line.strip()]
        bullets = [b for b in bullets if b][:request.max_points]
        
        response_obj = SummarizerResponse(
            id=str(uuid.uuid4()),
            original_text=request.text,
            summary=bullets,
            timestamp=datetime.utcnow()
        )
        
        # Store in DB (optional)
        await save_to_db('summaries', response_obj.dict(by_alias=False, exclude_unset=True))
        
        return response_obj
    except Exception as e:
        logger.error(f"Summarizer endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/mcq", response_model=MCQResponse)
async def mcq_endpoint(request: MCQRequest):
    """Generate multiple choice questions on a topic"""
    try:
        prompt = f"""Generate {request.num_questions} multiple choice questions on the topic: {request.topic}

For each question, provide:
1. The question text
2. Four options (A, B, C, D)
3. The correct answer letter
4. A brief explanation

Format your response as JSON array with objects containing: "question", "options" (array of {{letter, text}}), "correct_answer", "explanation"

Example format:
[{{"question": "...", "options": [{{"letter": "A", "text": "..."}}, ...], "correct_answer": "A", "explanation": "..."}}]

Generate the questions now:"""
        
        response_text = await call_llm(prompt, max_tokens=2500, temperature=0.5)
        
        # Extract JSON from response
        try:
            # Try to find JSON array in response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                questions_data = json.loads(json_str)
            else:
                questions_data = json.loads(response_text)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse MCQ JSON: {response_text}")
            raise HTTPException(status_code=500, detail="Failed to generate valid questions")
        
        # Convert to MCQuestion objects
        questions = []
        for q_data in questions_data[:request.num_questions]:
            options = [MCQOption(letter=opt["letter"], text=opt["text"]) for opt in q_data.get("options", [])]
            questions.append(MCQuestion(
                question=q_data.get("question", ""),
                options=options,
                correct_answer=q_data.get("correct_answer", ""),
                explanation=q_data.get("explanation", "")
            ))
        
        response_obj = MCQResponse(
            id=str(uuid.uuid4()),
            topic=request.topic,
            questions=questions,
            timestamp=datetime.utcnow()
        )
        
        # Store in DB (optional)
        await save_to_db('mcq_responses', response_obj.dict(by_alias=False, exclude_unset=True))
        
        return response_obj
    except Exception as e:
        logger.error(f"MCQ endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/explain-code", response_model=CodeExplainerResponse)
async def code_explainer_endpoint(request: CodeExplainerRequest):
    """Explain code snippets with detailed breakdown"""
    try:
        prompt = f"""Explain the following {request.language} code in detail.
Include:
1. What the code does at a high level
2. Explanation of key variables and functions
3. Step-by-step breakdown of logic
4. Any important patterns or concepts used
5. Potential improvements or edge cases to consider

Code:
```{request.language}
{request.code}
```

Provide a clear, educational explanation:"""
        
        explanation = await call_llm(prompt, max_tokens=2000)
        
        response_obj = CodeExplainerResponse(
            id=str(uuid.uuid4()),
            code=request.code,
            language=request.language,
            explanation=explanation,
            timestamp=datetime.utcnow()
        )
        
        # Store in DB (optional)
        await save_to_db('code_explanations', response_obj.dict(by_alias=False, exclude_unset=True))
        
        return response_obj
    except Exception as e:
        logger.error(f"Code explainer endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Include the router in the main app
app.include_router(api_router)

# Include enhanced v2 endpoints (file upload, advanced features)
try:
    from endpoints import enhanced_router
    app.include_router(enhanced_router)
    logger.info("Enhanced v2 endpoints loaded (file upload support)")
except ImportError as e:
    logger.warning(f"Enhanced endpoints not available: {str(e)}")

# Include V3 endpoints (auth, gamification, advanced code analysis)
try:
    import endpoints_v3
    
    # Monkey-patch to inject database into all V3 endpoints
    original_signup = endpoints_v3.signup
    original_login = endpoints_v3.login
    original_get_user_info = endpoints_v3.get_current_user_info
    original_get_stats = endpoints_v3.get_user_stats
    original_get_leaderboard = endpoints_v3.get_leaderboard
    original_analyze_code = endpoints_v3.analyze_code
    
    async def signup_with_db(user_data, db_param=None):
        return await original_signup(user_data, db=db)
    
    async def login_with_db(login_data, db_param=None):
        return await original_login(login_data, db=db)
    
    async def get_stats_with_db(current_user, db_param=None):
        return await original_get_stats(current_user, db=db)
    
    async def get_leaderboard_with_db(period="monthly", limit=10, db_param=None):
        return await original_get_leaderboard(period, limit, db=db)
    
    async def analyze_code_with_db(code=None, file=None, language="python", current_user=None, db_param=None):
        return await original_analyze_code(code, file, language, current_user, db=db)
    
    # Replace with patched versions
    endpoints_v3.signup = signup_with_db
    endpoints_v3.login = login_with_db
    endpoints_v3.get_user_stats = get_stats_with_db
    endpoints_v3.get_leaderboard = get_leaderboard_with_db
    endpoints_v3.analyze_code = analyze_code_with_db
    
    app.include_router(endpoints_v3.v3_router)
    logger.info("V3 endpoints loaded (Auth + Gamification + Advanced Code Analysis)")
    
    if mongodb_available:
        logger.info("V3 features fully enabled with MongoDB")
    else:
        logger.warning("V3 auth/gamification require MongoDB - some features limited")
except ImportError as e:
    logger.warning(f"V3 endpoints not available: {str(e)}")

# Add middleware (order matters!)
# 1. CORS - must be first for preflight requests
cors_origins = os.environ.get('CORS_ORIGINS', '*').split(',')
if IS_PRODUCTION and '*' in cors_origins:
    logger.warning("CORS is set to '*' in production - this is insecure!")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[origin.strip() for origin in cors_origins],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)

# 2. GZip compression for responses
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 3. Trusted Host middleware for production
if IS_PRODUCTION:
    allowed_hosts = os.environ.get('ALLOWED_HOSTS', '').split(',')
    if allowed_hosts and allowed_hosts[0]:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=[host.strip() for host in allowed_hosts]
        )

# 4. Rate limiting middleware
rpm = int(os.environ.get('RATE_LIMIT_PER_MINUTE', 60))
rph = int(os.environ.get('RATE_LIMIT_PER_HOUR', 1000))
if IS_PRODUCTION or os.environ.get('ENABLE_RATE_LIMIT', 'False').lower() == 'true':
    app.add_middleware(RateLimitMiddleware, rpm=rpm, rph=rph)
    logger.info(f"Rate limiting enabled: {rpm} req/min, {rph} req/hour")

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info(f"Starting EduFlow API in {ENV} mode")
    logger.info(f"LLM Provider: {DEFAULT_LLM_PROVIDER or 'NOT CONFIGURED'}")
    logger.info(f"Database: {'Available' if mongodb_available else 'Not configured (optional)'}")
    
    if mongodb_available and client:
        try:
            # Test database connection
            await client.admin.command('ping')
            logger.info("MongoDB connection established")
        except Exception as e:
            logger.warning(f"MongoDB ping failed: {str(e)} - continuing without database")
            global mongodb_available
            mongodb_available = False

@app.on_event("shutdown")
async def shutdown_event():
    """Graceful shutdown - close all connections"""
    logger.info("Shutting down EduFlow API...")
    if client:
        try:
            client.close()
            logger.info("MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")

# Production server runner
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0' if IS_PRODUCTION else '127.0.0.1')
    
    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        reload=not IS_PRODUCTION,
        log_level="info" if not IS_PRODUCTION else "warning",
        access_log=not IS_PRODUCTION,
        workers=1 if not IS_PRODUCTION else int(os.getenv('WORKERS', 4))
    )
