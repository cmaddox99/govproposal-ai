# GovProposalAI

AI-powered government proposal management platform with RBAC, MFA, and intelligent proposal scoring.

## Features

- **Role-Based Access Control (RBAC)**: Member, Admin, Owner, and Super User roles
- **Multi-Factor Authentication (MFA)**: TOTP-based with recovery codes
- **Proposal Scoring**: AI-powered multi-factor scoring with weighted factors
- **Color Team Readiness**: Pink, Red, Gold team review indicators
- **Audit Logging**: Comprehensive security event tracking
- **Benchmarks**: Historical comparison and trend analysis

## Tech Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **AI**: Claude API (Anthropic)
- **Infrastructure**: Docker, Redis

## Quick Start

### Prerequisites

- Docker & Docker Compose
- (Optional) Node.js 20+ and Python 3.11+ for local development

### 1. Clone and Configure

```bash
git clone https://github.com/cmaddox99/govproposal-ai.git
cd govproposal-ai

# Copy environment template
cp .env.example .env

# Edit .env with your values (especially JWT_SECRET_KEY and ANTHROPIC_API_KEY)
```

### 2. Generate Secrets

```bash
# Generate a secure JWT secret
openssl rand -hex 32
```

### 3. Run with Docker

```bash
# Production mode
docker-compose up -d

# Development mode (with hot reload)
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Development Setup

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start dev server
uvicorn govproposal.main:app --reload
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### Running Tests

```bash
# Backend tests
cd backend
python -m pytest tests/ -v

# Frontend type check
cd frontend
npx tsc --noEmit
```

## Project Structure

```
govproposal-ai/
├── backend/
│   ├── src/govproposal/
│   │   ├── identity/      # Auth, MFA, RBAC, sessions
│   │   ├── security/      # Audit logs, incidents
│   │   ├── scoring/       # Proposal scoring, benchmarks
│   │   └── db/            # Database configuration
│   ├── tests/
│   └── alembic/           # Database migrations
├── frontend/
│   └── src/
│       ├── app/           # Next.js pages
│       ├── components/    # React components
│       ├── lib/           # API client
│       └── types/         # TypeScript types
├── docker-compose.yml
└── .env.example
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `JWT_SECRET_KEY` | 256-bit secret for JWT signing | Yes |
| `ANTHROPIC_API_KEY` | Claude API key for AI scoring | For AI features |
| `CORS_ORIGINS` | Allowed frontend origins | Yes |
| `REDIS_URL` | Redis connection string | Optional |

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/mfa/setup` - Setup MFA
- `POST /api/v1/auth/mfa/challenge` - Verify MFA code

### Scoring
- `POST /api/v1/proposals/{id}/score/calculate` - Calculate proposal score
- `GET /api/v1/proposals/{id}/score` - Get current score
- `GET /api/v1/proposals/{id}/score/improvements` - Get improvement suggestions
- `POST /api/v1/proposals/{id}/score/readiness/{team}/check` - Check team readiness

### Admin
- `GET /api/v1/organizations/{id}/users` - List org users
- `POST /api/v1/organizations/{id}/users/invite` - Invite user
- `GET /api/v1/organizations/{id}/audit-logs` - View audit logs

## License

Proprietary - All rights reserved
