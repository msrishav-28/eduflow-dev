"""
User Model
Defines user data structure for authentication and gamification
"""
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserCreate(BaseModel):
    """User creation request"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    display_name: Optional[str] = Field(None, min_length=2, max_length=50)
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class UserInDB(BaseModel):
    """User as stored in database"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    password_hash: str
    display_name: str
    points: int = 0
    level: int = 1
    badges: List[str] = []
    streak_days: int = 0
    last_activity_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    total_activities: int = 0
    
    # Activity counts
    qa_count: int = 0
    summarize_count: int = 0
    mcq_count: int = 0
    code_explain_count: int = 0
    code_fix_count: int = 0
    
    # Feature unlocks (point-based rewards)
    max_file_size: int = 50000  # characters
    max_mcq_questions: int = 20
    max_summary_points: int = 20
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserPublic(BaseModel):
    """User data returned to client (no sensitive info)"""
    id: str
    email: EmailStr
    display_name: str
    points: int
    level: int
    badges: List[str]
    streak_days: int
    created_at: datetime
    total_activities: int
    qa_count: int
    summarize_count: int
    mcq_count: int
    code_explain_count: int
    code_fix_count: int
    max_file_size: int
    max_mcq_questions: int
    max_summary_points: int


class UserStats(BaseModel):
    """Detailed user statistics"""
    points: int
    level: int
    level_name: str
    points_to_next_level: int
    badges: List[dict]  # {name, description, icon, earned_at}
    streak_days: int
    total_activities: int
    activities_breakdown: dict
    feature_unlocks: dict
    rank: Optional[int] = None


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
