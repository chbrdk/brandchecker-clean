#!/bin/bash

echo "🚀 Starting Brandchecker Container..."

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install it first."
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Create shared directory if it doesn't exist
mkdir -p shared

# Start the containers
echo "📦 Starting containers..."
docker-compose up -d

# Wait a moment for containers to start
sleep 5

# Check container status
echo "🔍 Checking container status..."
docker-compose ps

echo ""
echo "✅ Brandchecker Container started successfully!"
echo ""
echo "📋 Service URLs:"
echo "   n8n:     http://localhost:5680 (admin / brandchecker123)"
echo "   Python:  http://localhost:8000"
echo ""
echo "📝 Useful commands:"
echo "   View logs:     docker-compose logs -f"
echo "   Stop:          docker-compose down"
echo "   Restart:       docker-compose restart"
echo "" 