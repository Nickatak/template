#!/bin/bash
# Setup script for test dependencies and environment

echo "🧪 Setting up authentication E2E tests..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install/upgrade dependencies
echo "Installing test dependencies..."
pip install -q -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install --with-deps

# Apply migrations
echo "Applying Django migrations..."
python manage.py migrate

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run tests:"
echo "   make test              # Run all tests"
echo "   make test-api          # Run API tests only"
echo "   make test-e2e          # Run E2E tests (requires servers running)"
echo ""
echo "📖 For more info, see TESTING.md"
