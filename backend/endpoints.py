"""
Enhanced API Endpoints
Supports file uploads, advanced summarization, and MCQ generation
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import uuid
from datetime import datetime
import logging

from file_processor import process_uploaded_file, validate_text_length, chunk_text
from llm_service import call_llm, generate_summary, generate_mcq_advanced

logger = logging.getLogger(__name__)

# Create enhanced router
enhanced_router = APIRouter(prefix="/api/v2")


# Models for enhanced endpoints
class SummarizerAdvancedRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=50000)
    style: str = Field(default="balanced", description="short_notes, long_notes, balanced, bullet_points, detailed")
    max_points: int = Field(default=5, ge=1, le=20)
    
    @validator('style')
    def validate_style(cls, v):
        allowed = ['short_notes', 'long_notes', 'balanced', 'bullet_points', 'detailed']
        if v not in allowed:
            raise ValueError(f'Style must be one of: {", ".join(allowed)}')
        return v


class SummarizerAdvancedResponse(BaseModel):
    id: str
    original_length: int
    summary: List[str]
    style: str
    timestamp: datetime
    source: str  # "text" or "file"


class MCQAdvancedRequest(BaseModel):
    text: str = Field(..., min_length=50, max_length=50000)
    num_questions: int = Field(default=5, ge=1, le=20)
    difficulty: str = Field(default="medium", description="easy, medium, hard")
    question_type: str = Field(default="mixed", description="factual, conceptual, application, mixed")
    
    @validator('difficulty')
    def validate_difficulty(cls, v):
        allowed = ['easy', 'medium', 'hard']
        if v not in allowed:
            raise ValueError(f'Difficulty must be one of: {", ".join(allowed)}')
        return v
    
    @validator('question_type')
    def validate_type(cls, v):
        allowed = ['factual', 'conceptual', 'application', 'mixed']
        if v not in allowed:
            raise ValueError(f'Question type must be one of: {", ".join(allowed)}')
        return v


class MCQOption(BaseModel):
    letter: str
    text: str


class MCQuestion(BaseModel):
    question: str
    options: List[MCQOption]
    correct_answer: str
    explanation: str


class MCQAdvancedResponse(BaseModel):
    id: str
    source_length: int
    questions: List[MCQuestion]
    difficulty: str
    question_type: str
    timestamp: datetime
    source: str  # "text" or "file"


# Enhanced Summarizer Endpoint with File Upload
@enhanced_router.post("/summarize", response_model=SummarizerAdvancedResponse)
async def summarize_advanced(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    style: str = Form("balanced"),
    max_points: int = Form(5)
):
    """
    Advanced summarizer with file upload support
    
    - Accepts direct text OR file upload (PDF, DOCX, TXT)
    - Multiple summary styles: short_notes, long_notes, balanced, bullet_points, detailed
    - Handles long documents with smart chunking
    """
    try:
        # Get text from either direct input or file
        source_type = "text"
        if file:
            if not file.filename:
                raise HTTPException(status_code=400, detail="No file provided")
            
            # Read file content
            file_content = await file.read()
            extracted_text, file_type = process_uploaded_file(file.filename, file_content)
            text = extracted_text
            source_type = f"file ({file_type})"
            logger.info(f"Processed {file_type} file: {file.filename}, extracted {len(text)} chars")
        
        if not text:
            raise HTTPException(status_code=400, detail="Either text or file must be provided")
        
        # Validate text length
        is_valid, message = validate_text_length(text, max_length=50000)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # Handle very long texts by chunking
        if len(text) > 8000:
            chunks = chunk_text(text, chunk_size=6000, overlap=200)
            logger.info(f"Text split into {len(chunks)} chunks for processing")
            
            # Summarize each chunk
            all_summaries = []
            for i, chunk in enumerate(chunks):
                chunk_summary = await generate_summary(chunk, style, max_points=max(3, max_points // len(chunks)))
                all_summaries.extend(chunk_summary)
            
            # Now summarize the summaries to get final points
            combined = "\n".join(all_summaries)
            final_summary = await generate_summary(combined, style, max_points)
        else:
            # Direct summarization for shorter texts
            final_summary = await generate_summary(text, style, max_points)
        
        response_obj = SummarizerAdvancedResponse(
            id=str(uuid.uuid4()),
            original_length=len(text),
            summary=final_summary,
            style=style,
            timestamp=datetime.utcnow(),
            source=source_type
        )
        
        return response_obj
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Summarizer endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Enhanced MCQ Generator with File Upload
@enhanced_router.post("/mcq", response_model=MCQAdvancedResponse)
async def generate_mcq_advanced_endpoint(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    num_questions: int = Form(5),
    difficulty: str = Form("medium"),
    question_type: str = Form("mixed")
):
    """
    Advanced MCQ generator with file upload support
    
    - Accepts direct text OR file upload (PDF, DOCX, TXT)
    - Difficulty levels: easy, medium, hard
    - Question types: factual, conceptual, application, mixed
    - Handles long documents intelligently
    """
    try:
        # Get text from either direct input or file
        source_type = "text"
        if file:
            if not file.filename:
                raise HTTPException(status_code=400, detail="No file provided")
            
            # Read file content
            file_content = await file.read()
            extracted_text, file_type = process_uploaded_file(file.filename, file_content)
            text = extracted_text
            source_type = f"file ({file_type})"
            logger.info(f"Processed {file_type} file: {file.filename}, extracted {len(text)} chars")
        
        if not text:
            raise HTTPException(status_code=400, detail="Either text or file must be provided")
        
        # Validate text length
        is_valid, message = validate_text_length(text, max_length=50000)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # Truncate if too long (take first 5000 chars for MCQ generation)
        if len(text) > 5000:
            text = text[:5000]
            logger.info(f"Text truncated to 5000 chars for MCQ generation")
        
        # Generate MCQs
        questions_data = await generate_mcq_advanced(
            text, 
            num_questions=num_questions,
            difficulty=difficulty,
            question_type=question_type
        )
        
        # Convert to MCQuestion objects
        questions = []
        for q_data in questions_data:
            options = [
                MCQOption(letter=opt["letter"], text=opt["text"]) 
                for opt in q_data.get("options", [])
            ]
            questions.append(MCQuestion(
                question=q_data.get("question", ""),
                options=options,
                correct_answer=q_data.get("correct_answer", ""),
                explanation=q_data.get("explanation", "")
            ))
        
        response_obj = MCQAdvancedResponse(
            id=str(uuid.uuid4()),
            source_length=len(text),
            questions=questions,
            difficulty=difficulty,
            question_type=question_type,
            timestamp=datetime.utcnow(),
            source=source_type
        )
        
        return response_obj
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"MCQ endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Quick endpoint for just text (backward compatible)
@enhanced_router.post("/summarize/text", response_model=SummarizerAdvancedResponse)
async def summarize_text_only(request: SummarizerAdvancedRequest):
    """Quick text-only summarization endpoint"""
    try:
        summary = await generate_summary(request.text, request.style, request.max_points)
        
        return SummarizerAdvancedResponse(
            id=str(uuid.uuid4()),
            original_length=len(request.text),
            summary=summary,
            style=request.style,
            timestamp=datetime.utcnow(),
            source="text"
        )
    except Exception as e:
        logger.error(f"Summarizer error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Quick endpoint for MCQ from text only
@enhanced_router.post("/mcq/text", response_model=MCQAdvancedResponse)
async def generate_mcq_text_only(request: MCQAdvancedRequest):
    """Quick text-only MCQ generation endpoint"""
    try:
        questions_data = await generate_mcq_advanced(
            request.text,
            num_questions=request.num_questions,
            difficulty=request.difficulty,
            question_type=request.question_type
        )
        
        questions = []
        for q_data in questions_data:
            options = [
                MCQOption(letter=opt["letter"], text=opt["text"]) 
                for opt in q_data.get("options", [])
            ]
            questions.append(MCQuestion(
                question=q_data.get("question", ""),
                options=options,
                correct_answer=q_data.get("correct_answer", ""),
                explanation=q_data.get("explanation", "")
            ))
        
        return MCQAdvancedResponse(
            id=str(uuid.uuid4()),
            source_length=len(request.text),
            questions=questions,
            difficulty=request.difficulty,
            question_type=request.question_type,
            timestamp=datetime.utcnow(),
            source="text"
        )
    except Exception as e:
        logger.error(f"MCQ error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
