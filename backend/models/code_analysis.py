"""
Code Analysis Model
Defines structure for code analysis results
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class CodeError(BaseModel):
    """Individual code error/issue"""
    type: str  # syntax_error, logic_error, style, security, performance
    line: Optional[int] = None
    column: Optional[int] = None
    message: str
    severity: str  # high, medium, low
    suggestion: Optional[str] = None


class CodeCorrection(BaseModel):
    """Line-by-line correction"""
    line: int
    original: str
    corrected: str
    reason: str


class CodeAnalysisRequest(BaseModel):
    """Request for code analysis"""
    code: Optional[str] = None
    language: str = Field(..., description="Programming language")
    
    class Config:
        schema_extra = {
            "example": {
                "code": "def hello():\n    print('Hello World'",
                "language": "python"
            }
        }


class CodeAnalysisResponse(BaseModel):
    """Code analysis result"""
    id: str
    user_id: Optional[str] = None
    language: str
    has_errors: bool
    error_count: int
    errors: List[CodeError]
    quality_score: int  # 0-100
    explanation: str
    corrected_code: Optional[str] = None
    line_corrections: List[CodeCorrection]
    suggestions: List[str]
    performance_tips: List[str]
    security_issues: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Scoring breakdown
    score_breakdown: Dict[str, int] = {
        "syntax": 0,
        "logic": 0,
        "style": 0,
        "security": 0,
        "performance": 0
    }


# Supported languages
SUPPORTED_LANGUAGES = {
    "python": {"extensions": [".py"], "name": "Python"},
    "javascript": {"extensions": [".js", ".jsx"], "name": "JavaScript"},
    "typescript": {"extensions": [".ts", ".tsx"], "name": "TypeScript"},
    "java": {"extensions": [".java"], "name": "Java"},
    "cpp": {"extensions": [".cpp", ".cc", ".cxx"], "name": "C++"},
    "c": {"extensions": [".c", ".h"], "name": "C"},
    "csharp": {"extensions": [".cs"], "name": "C#"},
    "go": {"extensions": [".go"], "name": "Go"},
    "rust": {"extensions": [".rs"], "name": "Rust"},
    "php": {"extensions": [".php"], "name": "PHP"},
    "ruby": {"extensions": [".rb"], "name": "Ruby"},
    "swift": {"extensions": [".swift"], "name": "Swift"},
    "kotlin": {"extensions": [".kt"], "name": "Kotlin"},
    "scala": {"extensions": [".scala"], "name": "Scala"},
    "r": {"extensions": [".r", ".R"], "name": "R"},
    "sql": {"extensions": [".sql"], "name": "SQL"},
    "html": {"extensions": [".html", ".htm"], "name": "HTML"},
    "css": {"extensions": [".css"], "name": "CSS"},
}
