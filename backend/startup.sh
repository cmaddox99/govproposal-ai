#!/bin/bash
set -e

echo "=== GovProposalAI Backend Startup ==="
echo "PORT: ${PORT:-8000}"
echo "DATABASE_URL set: $(if [ -n "$DATABASE_URL" ]; then echo 'yes'; else echo 'no'; fi)"

# Run migrations
echo ""
echo "Running database migrations..."
if alembic upgrade head; then
    echo "Migrations completed successfully!"
else
    echo "WARNING: Migrations failed, but continuing to start server..."
    echo "You may need to run migrations manually once the database is available."
fi

# Start the application
echo ""
echo "Starting uvicorn server on port ${PORT:-8000}..."
exec uvicorn govproposal.main:app --host 0.0.0.0 --port ${PORT:-8000}
