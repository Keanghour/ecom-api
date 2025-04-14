# app/core/cors.py

from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    """Add CORS middleware to the FastAPI app."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Correct: it's a list, not a type
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
