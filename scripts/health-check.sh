#!/bin/bash

# Health Check Script for EduFlow
# Can be used for monitoring, load balancers, or cron jobs

BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"
FRONTEND_URL="${FRONTEND_URL:-http://localhost}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🏥 EduFlow Health Check"
echo "======================="
echo ""

# Function to check HTTP endpoint
check_endpoint() {
    local name=$1
    local url=$2
    local expected_status=${3:-200}
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
    
    if [ "$response" = "$expected_status" ]; then
        echo -e "${GREEN}✅ $name: OK ($response)${NC}"
        return 0
    else
        echo -e "${RED}❌ $name: FAILED ($response)${NC}"
        return 1
    fi
}

# Check backend health
echo "Checking Backend..."
check_endpoint "Backend Health" "$BACKEND_URL/health"
backend_health=$?

check_endpoint "Backend Readiness" "$BACKEND_URL/readiness"
backend_ready=$?

check_endpoint "Backend API" "$BACKEND_URL/api/"
backend_api=$?

echo ""

# Check frontend health
echo "Checking Frontend..."
check_endpoint "Frontend Health" "$FRONTEND_URL/health"
frontend_health=$?

echo ""

# Database check (if backend is ready)
if [ $backend_ready -eq 0 ]; then
    echo -e "${GREEN}✅ Database: Connected${NC}"
else
    echo -e "${RED}❌ Database: Connection issues${NC}"
fi

echo ""

# Overall status
if [ $backend_health -eq 0 ] && [ $frontend_health -eq 0 ] && [ $backend_ready -eq 0 ]; then
    echo -e "${GREEN}🎉 Overall Status: HEALTHY${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Overall Status: DEGRADED${NC}"
    exit 1
fi
