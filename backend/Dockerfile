# GovProposalAI Backend Dockerfile
# Build: 2026-02-10-v2 - Added opportunities and proposals modules
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    fastapi[standard]>=0.109.0 \
    uvicorn[standard]>=0.27.0 \
    sqlalchemy[asyncio]>=2.0.0 \
    asyncpg>=0.29.0 \
    alembic>=1.13.0 \
    pydantic>=2.5.0 \
    pydantic-settings>=2.1.0 \
    pyjwt[crypto]>=2.10.0 \
    argon2-cffi>=23.1.0 \
    pyotp>=2.9.0 \
    httpx>=0.26.0 \
    anthropic>=0.18.0 \
    python-multipart

# Copy application code - bust cache by copying all source
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./
COPY startup.sh ./

# Fix line endings and make startup script executable
RUN sed -i 's/\r$//' startup.sh && chmod +x startup.sh

# Set Python path
ENV PYTHONPATH=/app/src

# Expose port
EXPOSE 8000

# Health check with longer start period for migrations
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=5 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run startup script (handles migrations and starts uvicorn)
CMD ["./startup.sh"]
