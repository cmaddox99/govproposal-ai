# GovProposalAI Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir \
    fastapi[standard] \
    uvicorn[standard] \
    sqlalchemy[asyncio] \
    asyncpg \
    alembic \
    pydantic \
    pydantic-settings \
    python-jose[cryptography] \
    passlib[argon2] \
    argon2-cffi \
    pyotp \
    httpx \
    anthropic \
    redis \
    python-multipart \
    pyjwt

# Copy application code
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
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1

# Run startup script (handles migrations and starts uvicorn)
CMD ["./startup.sh"]
