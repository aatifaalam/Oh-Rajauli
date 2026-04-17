from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from . import models
from .db import engine
from .routers import booking, order

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Oh! Rajauli Backend", description="Backend API for food ordering and table booking.")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(booking.router)
app.include_router(order.router)

# Serve static frontend files
# Go up two directories from app to project root
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Mount static files directly on `/` and `/assets` to serve index.html 
if os.path.exists(os.path.join(FRONTEND_DIR, 'index.html')):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, 'assets')), name="assets")
    
    @app.get("/")
    def serve_frontend():
        from fastapi.responses import FileResponse
        return FileResponse(os.path.join(FRONTEND_DIR, 'index.html'))
