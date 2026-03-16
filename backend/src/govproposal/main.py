"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware

from govproposal.config import settings
from govproposal.db.redis import close_redis, get_redis
from govproposal.events.handlers import register_event_handlers
from govproposal.middleware.rate_limit import limiter

# Router imports
from govproposal.identity.admin_router import router as admin_router
from govproposal.identity.auth_router import router as auth_router
from govproposal.identity.org_router import router as org_router
from govproposal.identity.past_performance_router import router as past_performance_router
from govproposal.identity.platform_router import router as platform_router
from govproposal.scoring.router import router as scoring_router
from govproposal.security.router import audit_router
from govproposal.opportunities.router import router as opportunities_router
from govproposal.proposals.router import router as proposals_router
from govproposal.assistant.router import router as assistant_router
from govproposal.compliance.router import router as compliance_router
from govproposal.analytics.router import router as analytics_router
from govproposal.notifications.router import router as notifications_router


# --- Security Headers Middleware ---

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response


# --- Lifespan ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    await get_redis()
    register_event_handlers()
    yield
    # Shutdown
    await close_redis()


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="AI-powered government proposal management platform",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware (bottom-up execution order: SecurityHeaders -> SlowAPI -> CORS)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(org_router)
app.include_router(past_performance_router)
app.include_router(admin_router)
app.include_router(platform_router)
app.include_router(audit_router)
app.include_router(scoring_router)
app.include_router(opportunities_router)
app.include_router(proposals_router)
app.include_router(assistant_router)
app.include_router(compliance_router)
app.include_router(analytics_router)
app.include_router(notifications_router)


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
