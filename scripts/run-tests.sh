#!/bin/bash

# TramitUp Test Runner Script

set -e

echo "🧪 Running TramitUp test suite..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Test frontend
echo "🔍 Running frontend tests..."
cd frontend

if npm run test; then
    print_status "Frontend tests passed"
else
    print_error "Frontend tests failed"
    FRONTEND_FAILED=1
fi

# Generate coverage report
if npm run test:coverage; then
    print_status "Frontend coverage report generated"
else
    print_warning "Frontend coverage report failed"
fi

cd ..

# Test backend
echo "🔍 Running backend tests..."
cd backend

if python -m pytest --cov=app --cov-report=html --cov-report=term; then
    print_status "Backend tests passed"
else
    print_error "Backend tests failed"
    BACKEND_FAILED=1
fi

cd ..

# Summary
echo ""
echo "📊 Test Summary:"
echo "=================="

if [ -z "$FRONTEND_FAILED" ]; then
    print_status "Frontend: All tests passed"
else
    print_error "Frontend: Some tests failed"
fi

if [ -z "$BACKEND_FAILED" ]; then
    print_status "Backend: All tests passed"
else
    print_error "Backend: Some tests failed"
fi

# Exit with error if any tests failed
if [ ! -z "$FRONTEND_FAILED" ] || [ ! -z "$BACKEND_FAILED" ]; then
    echo ""
    print_error "Some tests failed. Please fix them before committing."
    exit 1
else
    echo ""
    print_status "All tests passed! 🎉"
fi