"""
Vercel Serverless API Entry Point
This file makes the FastAPI app compatible with Vercel serverless functions
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from server import app

# Vercel expects 'app' or 'handler'
handler = app
