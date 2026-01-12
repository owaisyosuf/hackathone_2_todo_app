"""
FastAPI application entry point.

This module initializes the FastAPI application with middleware,
CORS configuration, and registers all API routers.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.config import settings

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="REST API for multi-user todo management with JWT authentication",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint for API health check.
    """
    return {
        "message": "Todo Application API",
        "version": settings.API_VERSION,
        "status": "operational",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


# Register API routers
from src.api import auth, tasks, chat, chat_simple

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(chat_simple.router, prefix="/chat", tags=["Chat Simple"])


# Global exception handlers
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    Handle database integrity errors (e.g., duplicate email registration).
    """
    if "users.email" in str(exc.orig):
        return JSONResponse(
            status_code=400,
            content={"detail": "Email already exists"},
        )
    return JSONResponse(
        status_code=503,
        content={"detail": "Service temporarily unavailable"},
    )


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handle HTTP exceptions (404, etc.) with custom format.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected exceptions.
    """
    # Log the actual error for debugging
    import traceback
    print(f"Unhandled exception: {exc}")
    print(f"Exception type: {type(exc)}")
    print(f"URL: {request.url}")
    print(f"Method: {request.method}")
    print(f"Traceback: {traceback.format_exc()}")

    return JSONResponse(
        status_code=503,
        content={"detail": f"Service temporarily unavailable: {str(exc)}"},
    )
