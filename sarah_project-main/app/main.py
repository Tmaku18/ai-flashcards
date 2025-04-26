from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Import for serving static files
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse

from .database import engine, Base

# Import routers
from .auth.router import router as auth_router
from .document.router import router as document_router
from .ai.router import router as ai_router
from .flashcards.router import router as flashcards_router
from .study.router import router as study_router
from .dashboard.router import router as dashboard_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Create upload directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

app = FastAPI(
    title="Flashcard App API",
    description="API for the Flashcard Application with AI-powered flashcard generation",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(document_router, prefix="/api")
app.include_router(ai_router, prefix="/api")
app.include_router(flashcards_router, prefix="/api")
app.include_router(study_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")


@app.get("/")
async def root():
    """Serve the frontend index page"""
    index_path = os.path.join(os.getcwd(), "frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        # Fallback to API message if frontend is not built
        return {"message": "Welcome to Flashcard App API"}


@app.get("/dashboard")
@app.get("/dashboard/sets")
@app.get("/dashboard/sets/{set_id}")
@app.get("/dashboard/study")
@app.get("/dashboard/study/session/{session_id}")
@app.get("/dashboard/upload")
@app.get("/dashboard/stats")
@app.get("/dashboard/settings")
@app.get("/dashboard/{path:path}")
async def dashboard(path: str = "", set_id: str = None, session_id: str = None):
    """Serve the dashboard page for all dashboard routes"""
    dashboard_path = os.path.join(os.getcwd(), "frontend", "dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    else:
        # Fallback to a simple message
        return HTMLResponse(
            content="<html><body><h1>Dashboard</h1><p>This is a placeholder for the dashboard. In a real application, this would be a dynamic page.</p><p><a href='/'>Back to Home</a></p></body></html>"
        )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Mount static files for the frontend
frontend_dir = os.path.join(os.getcwd(), "frontend")
if os.path.exists(os.path.join(frontend_dir, "_next")):
    app.mount(
        "/_next",
        StaticFiles(directory=os.path.join(frontend_dir, "_next")),
        name="next-static",
    )

if os.path.exists(os.path.join(frontend_dir, "public")):
    app.mount(
        "/public",
        StaticFiles(directory=os.path.join(frontend_dir, "public")),
        name="public",
    )
