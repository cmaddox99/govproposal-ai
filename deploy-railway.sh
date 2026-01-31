#!/bin/bash
# GovProposalAI - Railway Deployment Script

set -e

echo "=== GovProposalAI Railway Deployment ==="
echo ""

# Check if logged in
if ! railway whoami &>/dev/null; then
    echo "Step 1: Login to Railway"
    echo "------------------------"
    railway login
    echo ""
fi

echo "Step 2: Creating Railway Project"
echo "---------------------------------"
cd backend

# Initialize project if not already
if [ ! -f ".railway/config.json" ]; then
    railway init --name govproposal-ai
fi

echo ""
echo "Step 3: Adding PostgreSQL"
echo "-------------------------"
railway add --plugin postgresql
echo "PostgreSQL added!"

echo ""
echo "Step 4: Adding Redis"
echo "--------------------"
railway add --plugin redis
echo "Redis added!"

echo ""
echo "Step 5: Setting Environment Variables"
echo "--------------------------------------"
railway variables set JWT_SECRET_KEY="$(openssl rand -hex 32)"
railway variables set JWT_ALGORITHM="HS256"
railway variables set JWT_ACCESS_TOKEN_EXPIRE_MINUTES="30"
railway variables set JWT_REFRESH_TOKEN_EXPIRE_DAYS="7"
railway variables set MFA_ISSUER_NAME="GovProposalAI"
railway variables set DEBUG="false"
railway variables set CORS_ORIGINS='["https://your-vercel-app.vercel.app"]'
echo "Environment variables set!"

echo ""
echo "Step 6: Deploying Backend"
echo "-------------------------"
railway up --detach

echo ""
echo "=== Deployment Complete ==="
echo ""
echo "Next steps:"
echo "1. Get your backend URL: railway open"
echo "2. Run migrations: railway run alembic upgrade head"
echo "3. Update Vercel NEXT_PUBLIC_API_URL with your Railway URL"
echo ""
