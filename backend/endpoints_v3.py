"""
V3 Enhanced API Endpoints
Authentication, Gamification, Advanced Code Analysis
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import Optional, List
import logging

from auth import AuthService, get_current_user
from gamification import GamificationService
from code_analyzer import CodeAnalyzer
from file_processor import process_uploaded_file
from models.user import UserCreate, UserLogin, TokenResponse, UserInDB, UserStats
from models.activity import ActivityCreate
from models.code_analysis import CodeAnalysisRequest, CodeAnalysisResponse

logger = logging.getLogger(__name__)

# Create V3 router
v3_router = APIRouter(prefix="/api/v3")


# Dependency to get services (with or without MongoDB)
async def get_services(db=None):
    """Get auth and gamification services"""
    auth_service = AuthService(db)
    gamification_service = GamificationService(db)
    return auth_service, gamification_service


# ============================================
# AUTHENTICATION ENDPOINTS
# ============================================

@v3_router.post("/auth/signup", response_model=TokenResponse)
async def signup(user_data: UserCreate, db=None):
    """
    Register new user
    Requires: email, password (min 8 chars with uppercase, lowercase, digit)
    """
    try:
        auth_service = AuthService(db)
        return await auth_service.register_user(user_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@v3_router.post("/auth/login", response_model=TokenResponse)
async def login(login_data: UserLogin, db=None):
    """
    Login user
    Returns JWT token and user data
    """
    try:
        auth_service = AuthService(db)
        return await auth_service.login_user(login_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@v3_router.get("/auth/me")
async def get_current_user_info(
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Get current logged-in user info
    Requires: Bearer token in Authorization header
    """
    from auth import user_to_public
    return user_to_public(current_user)


# ============================================
# GAMIFICATION ENDPOINTS
# ============================================

@v3_router.get("/gamification/stats", response_model=UserStats)
async def get_user_stats(
    current_user: UserInDB = Depends(get_current_user),
    db=None
):
    """
    Get user's gamification stats
    Points, level, badges, rank, feature unlocks
    """
    try:
        gamification = GamificationService(db)
        stats = await gamification.get_user_stats(str(current_user.id))
        if not stats:
            raise HTTPException(status_code=404, detail="Stats not found")
        return stats
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@v3_router.get("/gamification/leaderboard")
async def get_leaderboard(
    period: str = "monthly",
    limit: int = 10,
    db=None
):
    """
    Get leaderboard
    period: monthly (resets monthly) or all_time
    """
    try:
        if period not in ["monthly", "all_time"]:
            raise HTTPException(status_code=400, detail="Period must be 'monthly' or 'all_time'")
        
        gamification = GamificationService(db)
        leaderboard = await gamification.get_leaderboard(period=period, limit=limit)
        return {
            "period": period,
            "leaderboard": leaderboard
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Leaderboard error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# ENHANCED CODE ANALYZER ENDPOINTS
# ============================================

@v3_router.post("/code/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(
    code: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    language: str = Form("python"),
    current_user: Optional[UserInDB] = Depends(get_current_user),
    db=None
):
    """
    Advanced code analysis with file upload support
    
    Features:
    - Error detection (syntax, logic, style, security, performance)
    - Quality scoring (0-100)
    - Line-by-line corrections
    - Performance optimization tips
    - Security issue detection
    
    Upload code file OR paste code directly
    Supports: Python, JavaScript, TypeScript, Java, C++, C, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, etc.
    """
    try:
        # Get code from file or form
        if file:
            if not file.filename:
                raise HTTPException(status_code=400, detail="No file provided")
            
            file_content = await file.read()
            
            # Try to extract text
            try:
                code = file_content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    code = file_content.decode('latin-1')
                except:
                    raise HTTPException(status_code=400, detail="Unable to decode file. Please use UTF-8 encoded text files.")
            
            # Auto-detect language from filename
            analyzer = CodeAnalyzer()
            detected_lang = analyzer.detect_language_from_filename(file.filename)
            if detected_lang != "unknown":
                language = detected_lang
            
            logger.info(f"Analyzing code file: {file.filename}, detected language: {language}")
        
        if not code:
            raise HTTPException(status_code=400, detail="Either code or file must be provided")
        
        # Check file size limit
        if current_user:
            max_size = current_user.max_file_size
        else:
            max_size = 10000  # 10K chars for non-authenticated users
        
        if len(code) > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"Code too long ({len(code)} chars). Your limit: {max_size} chars. Earn points to unlock larger limits!"
            )
        
        # Analyze code
        analyzer = CodeAnalyzer()
        result = await analyzer.analyze_code(code, language, file.filename if file else None)
        
        # Log activity if user is authenticated
        if current_user and db:
            gamification = GamificationService(db)
            activity_result = await gamification.log_activity(
                user_id=str(current_user.id),
                activity_type="code_explain",
                metadata={
                    "language": language,
                    "quality_score": result.quality_score,
                    "error_count": result.error_count
                }
            )
            
            # Add activity result to response (for frontend notification)
            result.user_id = str(current_user.id)
            logger.info(f"Activity logged: {activity_result}")
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Code analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@v3_router.post("/code/quick-check")
async def quick_code_check(
    request: CodeAnalysisRequest,
    current_user: Optional[UserInDB] = Depends(get_current_user)
):
    """
    Quick code error check (faster, simpler)
    Returns basic error info without full analysis
    """
    try:
        analyzer = CodeAnalyzer()
        result = await analyzer.quick_check(request.code, request.language)
        return result
    except Exception as e:
        logger.error(f"Quick check error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# HELPER FUNCTION TO INJECT DB
# ============================================

def setup_v3_router(app, db=None):
    """
    Setup V3 router with database dependency
    Call this from main server.py
    """
    # Inject database into endpoints
    async def get_db():
        return db
    
    # Override dependencies
    v3_router.dependencies = [Depends(lambda: db)]
    
    app.include_router(v3_router)
    
    logger.info("V3 endpoints loaded (Auth + Gamification + Advanced Code Analysis)")
