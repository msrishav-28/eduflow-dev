"""
Code Analyzer Service
Advanced code analysis with error detection, quality scoring, line-by-line corrections
"""
import logging
import uuid
from datetime import datetime
from typing import List, Tuple

from llm_service import call_llm
from models.code_analysis import (
    CodeError, CodeCorrection, CodeAnalysisResponse,
    SUPPORTED_LANGUAGES
)

logger = logging.getLogger(__name__)


class CodeAnalyzer:
    """Advanced code analyzer with AI-powered analysis"""
    
    @staticmethod
    def detect_language_from_filename(filename: str) -> str:
        """Detect programming language from file extension"""
        extension = '.' + filename.split('.')[-1] if '.' in filename else ''
        extension = extension.lower()
        
        for lang, data in SUPPORTED_LANGUAGES.items():
            if extension in data["extensions"]:
                return lang
        
        return "unknown"
    
    async def analyze_code(
        self,
        code: str,
        language: str,
        filename: str = None
    ) -> CodeAnalysisResponse:
        """
        Comprehensive code analysis
        Returns errors, corrections, quality score, and suggestions
        """
        # Auto-detect language from filename if provided
        if filename and language == "unknown":
            language = self.detect_language_from_filename(filename)
        
        if language not in SUPPORTED_LANGUAGES and language != "unknown":
            language = "unknown"
        
        lang_name = SUPPORTED_LANGUAGES.get(language, {}).get("name", language)
        
        # Build comprehensive analysis prompt
        prompt = f"""Analyze this {lang_name} code comprehensively and provide:

1. **Errors & Issues**: List all syntax errors, logic errors, style issues, security vulnerabilities, and performance problems
2. **Line-by-line corrections**: For each error, provide the corrected line
3. **Quality Score**: Rate the code 0-100 based on:
   - Syntax correctness (20 points)
   - Logic correctness (20 points)
   - Code style & readability (20 points)
   - Security (20 points)
   - Performance (20 points)
4. **Corrected Code**: Provide the fully corrected version
5. **Suggestions**: List improvements and best practices
6. **Performance Tips**: Specific optimization suggestions

CODE:
```{language}
{code}
```

Respond in this exact JSON format:
{{
  "errors": [
    {{"type": "syntax_error|logic_error|style|security|performance", "line": 5, "column": 10, "message": "Error description", "severity": "high|medium|low", "suggestion": "How to fix"}}
  ],
  "line_corrections": [
    {{"line": 5, "original": "bad code", "corrected": "good code", "reason": "Why this is better"}}
  ],
  "quality_score": 75,
  "score_breakdown": {{
    "syntax": 18,
    "logic": 20,
    "style": 15,
    "security": 20,
    "performance": 12
  }},
  "corrected_code": "Full corrected code here",
  "explanation": "Overall explanation of the code and its issues",
  "suggestions": ["Suggestion 1", "Suggestion 2"],
  "performance_tips": ["Tip 1", "Tip 2"],
  "security_issues": ["Issue 1", "Issue 2"]
}}

Provide ONLY the JSON response, no markdown formatting."""
        
        try:
            # Call LLM for analysis
            response_text = await call_llm(prompt, temperature=0.3, max_tokens=4000)
            
            # Parse JSON response
            import json
            
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                analysis_data = json.loads(json_str)
            else:
                # Try parsing entire response
                analysis_data = json.loads(response_text)
            
            # Convert to models
            errors = [
                CodeError(**err) for err in analysis_data.get("errors", [])
            ]
            
            line_corrections = [
                CodeCorrection(**corr) for corr in analysis_data.get("line_corrections", [])
            ]
            
            # Build response
            response = CodeAnalysisResponse(
                id=str(uuid.uuid4()),
                language=language,
                has_errors=len(errors) > 0,
                error_count=len(errors),
                errors=errors,
                quality_score=analysis_data.get("quality_score", 50),
                explanation=analysis_data.get("explanation", "Code analysis completed"),
                corrected_code=analysis_data.get("corrected_code"),
                line_corrections=line_corrections,
                suggestions=analysis_data.get("suggestions", []),
                performance_tips=analysis_data.get("performance_tips", []),
                security_issues=analysis_data.get("security_issues", []),
                score_breakdown=analysis_data.get("score_breakdown", {
                    "syntax": 0, "logic": 0, "style": 0, "security": 0, "performance": 0
                })
            )
            
            logger.info(f"Code analyzed: {language}, score: {response.quality_score}, errors: {response.error_count}")
            return response
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse code analysis JSON: {str(e)}")
            logger.error(f"Response was: {response_text[:500]}")
            
            # Return basic analysis
            return await self._fallback_analysis(code, language, response_text)
        
        except Exception as e:
            logger.error(f"Code analysis error: {str(e)}")
            raise
    
    async def _fallback_analysis(
        self,
        code: str,
        language: str,
        llm_response: str
    ) -> CodeAnalysisResponse:
        """Fallback analysis when JSON parsing fails"""
        # Extract what we can from the response
        has_errors = any(keyword in llm_response.lower() 
                        for keyword in ['error', 'issue', 'problem', 'bug', 'incorrect'])
        
        # Estimate quality score from keywords
        quality_score = 70
        if 'excellent' in llm_response.lower() or 'perfect' in llm_response.lower():
            quality_score = 90
        elif 'good' in llm_response.lower():
            quality_score = 75
        elif 'poor' in llm_response.lower() or 'bad' in llm_response.lower():
            quality_score = 40
        
        return CodeAnalysisResponse(
            id=str(uuid.uuid4()),
            language=language,
            has_errors=has_errors,
            error_count=llm_response.lower().count('error'),
            errors=[],
            quality_score=quality_score,
            explanation=llm_response[:1000],  # Use LLM response as explanation
            corrected_code=None,
            line_corrections=[],
            suggestions=[],
            performance_tips=[],
            security_issues=[],
            score_breakdown={
                "syntax": quality_score // 5,
                "logic": quality_score // 5,
                "style": quality_score // 5,
                "security": quality_score // 5,
                "performance": quality_score // 5
            }
        )
    
    async def quick_check(self, code: str, language: str) -> dict:
        """Quick code check for basic errors (faster, simpler)"""
        prompt = f"""Quickly check this {language} code for errors.
List up to 5 critical issues only.

CODE:
```{language}
{code}
```

Respond in JSON format:
{{"has_errors": true/false, "error_count": 3, "errors": ["error 1", "error 2"]}}"""
        
        try:
            response = await call_llm(prompt, temperature=0.2, max_tokens=500)
            
            import json
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            
            return {"has_errors": False, "error_count": 0, "errors": []}
        
        except Exception as e:
            logger.error(f"Quick check error: {str(e)}")
            return {"has_errors": False, "error_count": 0, "errors": []}
