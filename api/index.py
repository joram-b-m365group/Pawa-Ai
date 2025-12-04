# Vercel serverless function that wraps the FastAPI backend
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from production_api import app

# Vercel needs this
handler = app
