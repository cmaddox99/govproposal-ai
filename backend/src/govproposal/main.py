"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from govproposal.config import settings
from govproposal.identity.admin_router import router as admin_router
from govproposal.identity.auth_router import router as auth_router
from govproposal.identity.org_router import router as org_router
from govproposal.identity.platform_router import router as platform_router
from govproposal.scoring.router import router as scoring_router
from govproposal.security.router import audit_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="AI-powered government proposal management platform",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(org_router)
app.include_router(admin_router)
app.include_router(platform_router)
app.include_router(audit_router)
app.include_router(scoring_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.version}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.version,
        "docs": "/docs",
    }
