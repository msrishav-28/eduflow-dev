"""
LLM Service Module
Handles all LLM interactions with different providers
"""
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Configure LLM Providers
openai_api_key = os.environ.get('OPENAI_API_KEY')
gemini_api_key = os.environ.get('GEMINI_API_KEY')
anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY')

if openai_api_key:
    import openai
    openai.api_key = openai_api_key

if gemini_api_key:
    import google.generativeai as genai
    genai.configure(api_key=gemini_api_key)


def get_available_llm_provider() -> Optional[str]:
    """Returns the available LLM provider in order of preference"""
    if gemini_api_key:
        return "gemini"
    elif openai_api_key:
        return "openai"
    elif anthropic_api_key:
        return "anthropic"
    return None


DEFAULT_LLM_PROVIDER = get_available_llm_provider()


async def call_llm(prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
    """Call LLM with automatic provider selection and fallback"""
    provider = DEFAULT_LLM_PROVIDER
    
    if not provider:
        raise Exception("No LLM API key configured. Please set GEMINI_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY")
    
    try:
        if provider == "gemini":
            return await call_gemini(prompt, temperature, max_tokens)
        elif provider == "openai":
            return await call_openai(prompt, temperature, max_tokens)
        elif provider == "anthropic":
            return await call_anthropic(prompt, temperature, max_tokens)
    except Exception as e:
        logger.error(f"LLM error with {provider}: {str(e)}")
        raise


async def call_gemini(prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
    """Call Google Gemini API"""
    if not gemini_api_key:
        raise Exception("Gemini API key not configured")
    
    try:
        import google.generativeai as genai
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
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
    """Call OpenAI API"""
    if not openai_api_key:
        raise Exception("OpenAI API key not configured")
    
    try:
        import openai
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
    """Call Anthropic Claude API"""
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


async def generate_summary(text: str, style: str = "balanced", max_points: int = 5) -> list:
    """
    Generate summary with different styles
    Styles: short_notes, long_notes, balanced, bullet_points, detailed
    """
    style_instructions = {
        "short_notes": f"Create {max_points} very concise bullet point notes (5-10 words each). Focus on key facts only.",
        "long_notes": f"Create {max_points} comprehensive detailed notes (2-3 sentences each). Include context and explanations.",
        "balanced": f"Create {max_points} balanced bullet points (1-2 sentences each). Include main ideas and key details.",
        "bullet_points": f"Create {max_points} clear bullet points highlighting the main topics.",
        "detailed": f"Create {max_points} detailed points with examples and explanations."
    }
    
    instruction = style_instructions.get(style, style_instructions["balanced"])
    
    prompt = f"""Summarize the following text.

{instruction}

Text:
{text}

Provide ONLY the bullet points, numbered 1-{max_points}. No introduction or conclusion."""
    
    response = await call_llm(prompt, max_tokens=2000, temperature=0.5)
    
    # Parse bullet points
    lines = response.split('\n')
    bullets = []
    for line in lines:
        line = line.strip()
        if line:
            # Remove numbering/bullets
            cleaned = line.lstrip('0123456789.-*•) ').strip()
            if cleaned:
                bullets.append(cleaned)
    
    return bullets[:max_points]


async def generate_mcq_advanced(
    text: str,
    num_questions: int = 5,
    difficulty: str = "medium",
    question_type: str = "mixed"
) -> list:
    """
    Generate MCQs with advanced options
    difficulty: easy, medium, hard
    question_type: factual, conceptual, application, mixed
    """
    difficulty_instructions = {
        "easy": "straightforward questions about basic facts and definitions",
        "medium": "questions requiring understanding and interpretation",
        "hard": "complex questions requiring analysis and application"
    }
    
    type_instructions = {
        "factual": "questions about specific facts, dates, names, and definitions",
        "conceptual": "questions about concepts, relationships, and understanding",
        "application": "questions requiring application of knowledge to scenarios",
        "mixed": "a mix of factual, conceptual, and application questions"
    }
    
    diff_instruction = difficulty_instructions.get(difficulty, difficulty_instructions["medium"])
    type_instruction = type_instructions.get(question_type, type_instructions["mixed"])
    
    prompt = f"""Generate {num_questions} multiple choice questions based on the following text.

Requirements:
- Difficulty: {difficulty} - {diff_instruction}
- Type: {question_type} - {type_instruction}
- Each question must have exactly 4 options (A, B, C, D)
- Clearly indicate the correct answer
- Provide a brief explanation for the correct answer

Text:
{text[:3000]}

Format your response as JSON array:
[
  {{
    "question": "Question text here?",
    "options": [
      {{"letter": "A", "text": "Option A"}},
      {{"letter": "B", "text": "Option B"}},
      {{"letter": "C", "text": "Option C"}},
      {{"letter": "D", "text": "Option D"}}
    ],
    "correct_answer": "A",
    "explanation": "Explanation here"
  }}
]

Generate the questions now:"""
    
    response = await call_llm(prompt, max_tokens=3000, temperature=0.6)
    
    # Extract JSON
    import json
    try:
        start_idx = response.find('[')
        end_idx = response.rfind(']') + 1
        if start_idx != -1 and end_idx > start_idx:
            json_str = response[start_idx:end_idx]
            questions_data = json.loads(json_str)
        else:
            questions_data = json.loads(response)
        
        return questions_data[:num_questions]
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse MCQ JSON: {response}")
        raise Exception("Failed to generate valid questions. Please try again.")
