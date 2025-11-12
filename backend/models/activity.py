"""
Activity Model
Tracks user activities for gamification
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from bson import ObjectId


class Activity(BaseModel):
    """Activity record"""
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    activity_type: str  # qa, summarize, mcq, code_explain, code_fix, file_upload, daily_login
    points_earned: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = {}
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class ActivityCreate(BaseModel):
    """Create activity request"""
    activity_type: str
    metadata: Optional[Dict[str, Any]] = {}


# Point values for different activities
ACTIVITY_POINTS = {
    "qa": 5,
    "summarize": 10,
    "mcq": 15,
    "code_explain": 10,
    "code_fix": 20,
    "file_upload": 5,
    "daily_login": 10,
    "streak_7": 50,
    "streak_30": 200,
    "quiz_complete": 25,
}

# Badge definitions
BADGES = {
    "beginner": {
        "name": "🏆 Beginner",
        "description": "Complete your first activity",
        "requirement": {"type": "total_activities", "count": 1}
    },
    "reader": {
        "name": "📚 Reader",
        "description": "Summarize 10 documents",
        "requirement": {"type": "summarize_count", "count": 10}
    },
    "scholar": {
        "name": "🎓 Scholar",
        "description": "Summarize 50 documents",
        "requirement": {"type": "summarize_count", "count": 50}
    },
    "coder": {
        "name": "💻 Coder",
        "description": "Analyze 20 code files",
        "requirement": {"type": "code_explain_count", "count": 20}
    },
    "debugger": {
        "name": "🐛 Debugger",
        "description": "Fix 10 code errors",
        "requirement": {"type": "code_fix_count", "count": 10}
    },
    "streak_master": {
        "name": "🔥 Streak Master",
        "description": "30-day activity streak",
        "requirement": {"type": "streak_days", "count": 30}
    },
    "quiz_master": {
        "name": "🎯 Quiz Master",
        "description": "Generate 50 quizzes",
        "requirement": {"type": "mcq_count", "count": 50}
    },
    "speed_learner": {
        "name": "⚡ Speed Learner",
        "description": "Ask 100 questions",
        "requirement": {"type": "qa_count", "count": 100}
    },
    "legend": {
        "name": "👑 Legend",
        "description": "Reach 10,000 points",
        "requirement": {"type": "points", "count": 10000}
    },
}

# Level thresholds
LEVELS = [
    {"level": 1, "name": "Newbie", "min_points": 0, "max_points": 100},
    {"level": 2, "name": "Learner", "min_points": 101, "max_points": 500},
    {"level": 3, "name": "Scholar", "min_points": 501, "max_points": 1000},
    {"level": 4, "name": "Expert", "min_points": 1001, "max_points": 5000},
    {"level": 5, "name": "Master", "min_points": 5001, "max_points": 999999},
]

# Feature unlock thresholds
FEATURE_UNLOCKS = {
    "file_size_boost_1": {
        "points": 500,
        "benefit": {"max_file_size": 100000},
        "name": "Larger Files (100K chars)"
    },
    "file_size_boost_2": {
        "points": 2000,
        "benefit": {"max_file_size": 200000},
        "name": "XL Files (200K chars)"
    },
    "mcq_boost": {
        "points": 1000,
        "benefit": {"max_mcq_questions": 50},
        "name": "More MCQs (50 questions)"
    },
    "summary_boost": {
        "points": 800,
        "benefit": {"max_summary_points": 50},
        "name": "Detailed Summaries (50 points)"
    },
}
