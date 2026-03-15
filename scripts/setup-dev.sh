#!/bin/bash

# TramitUp Development Setup Script

set -e  # Exit on any error

echo "🚀 Setting up TramitUp development environment..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 20+ first."
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.12+ first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "package.json" ] && [ ! -d "frontend" ]; then
    echo "❌ Please run this script from the TramitUp root directory."
    exit 1
fi

echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "🐍 Installing backend dependencies..."
cd backend
if command -v python3 &> /dev/null; then
    python3 -m pip install -r requirements.txt
else
    python -m pip install -r requirements.txt
fi
cd ..

echo "🔧 Setting up pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
else
    echo "⚠️  pre-commit not found. Install it with: pip install pre-commit"
fi

echo "📄 Copying environment file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual environment variables"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Supabase and Google AI credentials"
echo "2. Run 'make dev' to start both frontend and backend"
echo "3. Visit http://localhost:3000 to see the application"
echo ""
echo "Useful commands:"
echo "  make dev          - Start development servers"
echo "  make test         - Run all tests"
echo "  make lint         - Run linting"
echo "  make format       - Format code"
echo ""