"""
Authentication Service
Handles user registration, login, JWT tokens
"""
import os
import logging
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models.user import UserCreate, UserLogin, UserInDB, UserPublic, TokenResponse

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Security
security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        logger.error(f"JWT decode error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = None
) -> UserInDB:
    """
    Get current user from JWT token
    Usage: current_user = Depends(get_current_user)
    """
    token = credentials.credentials
    payload = decode_token(token)
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    # If MongoDB available, get fresh user data
    if db:
        from bson import ObjectId
        user_data = await db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return UserInDB(**user_data)
    
    # Otherwise return from token payload
    return UserInDB(**payload.get("user_data", {}))


def user_to_public(user: UserInDB) -> UserPublic:
    """Convert UserInDB to UserPublic (safe for client)"""
    return UserPublic(
        id=str(user.id),
        email=user.email,
        display_name=user.display_name,
        points=user.points,
        level=user.level,
        badges=user.badges,
        streak_days=user.streak_days,
        created_at=user.created_at,
        total_activities=user.total_activities,
        qa_count=user.qa_count,
        summarize_count=user.summarize_count,
        mcq_count=user.mcq_count,
        code_explain_count=user.code_explain_count,
        code_fix_count=user.code_fix_count,
        max_file_size=user.max_file_size,
        max_mcq_questions=user.max_mcq_questions,
        max_summary_points=user.max_summary_points,
    )


class AuthService:
    """Authentication service"""
    
    def __init__(self, db=None):
        self.db = db
        self.mongodb_available = db is not None
    
    async def register_user(self, user_data: UserCreate) -> TokenResponse:
        """Register a new user"""
        if not self.mongodb_available:
            raise HTTPException(
                status_code=503,
                detail="Authentication requires MongoDB. Please configure MONGO_URL."
            )
        
        # Check if user exists
        existing_user = await self.db.users.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        
        # Create user
        user = UserInDB(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            display_name=user_data.display_name or user_data.email.split('@')[0],
        )
        
        # Insert to database
        result = await self.db.users.insert_one(user.dict(by_alias=True, exclude={"id"}))
        user.id = result.inserted_id
        
        # Create token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        logger.info(f"New user registered: {user.email}")
        
        return TokenResponse(
            access_token=access_token,
            user=user_to_public(user)
        )
    
    async def login_user(self, login_data: UserLogin) -> TokenResponse:
        """Login user and return token"""
        if not self.mongodb_available:
            raise HTTPException(
                status_code=503,
                detail="Authentication requires MongoDB. Please configure MONGO_URL."
            )
        
        # Find user
        user_data = await self.db.users.find_one({"email": login_data.email})
        if not user_data:
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password"
            )
        
        user = UserInDB(**user_data)
        
        # Verify password
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password"
            )
        
        # Update last activity
        await self.db.users.update_one(
            {"_id": user.id},
            {"$set": {"last_activity_date": datetime.utcnow()}}
        )
        
        # Create token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        logger.info(f"User logged in: {user.email}")
        
        return TokenResponse(
            access_token=access_token,
            user=user_to_public(user)
        )
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        """Get user by ID"""
        if not self.mongodb_available:
            return None
        
        from bson import ObjectId
        user_data = await self.db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return UserInDB(**user_data)
        return None
