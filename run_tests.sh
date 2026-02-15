#!/bin/bash
# Run integration tests with environment variables loaded

# Load environment variables from .env if it exists (check root and backend)
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
elif [ -f backend/.env ]; then
    export $(cat backend/.env | grep -v '^#' | xargs)
fi

# Check if API key is set
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ ERROR: OPENROUTER_API_KEY not set"
    echo ""
    echo "Please set your API key:"
    echo "  export OPENROUTER_API_KEY='your-key-here'"
    echo ""
    echo "Or add it to backend/.env:"
    echo "  echo 'OPENROUTER_API_KEY=your-key-here' > backend/.env"
    exit 1
fi

echo "🧪 Running Integration Tests..."
echo "📅 $(date)"
echo ""

# Run tests with conda environment
conda run -n Finance_env python tests/test_integration.py

echo ""
echo "✅ Test run complete!"
