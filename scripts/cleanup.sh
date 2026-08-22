#!/usr/bin/env bash
# YouTube AI Automation - Cleanup Script
# Removes temporary files and cache

echo "🧹 Cleaning up temporary files..."

# Clean Python cache
echo "Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# Clean Node cache
echo "Removing Node.js cache files..."
find . -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name ".npm" -type d -exec rm -rf {} + 2>/dev/null || true

# Clean temporary files
echo "Removing temporary files..."
rm -rf temp/* 2>/dev/null || true

# Clean logs (optional - comment if you want to keep them)
# rm -rf logs/* 2>/dev/null || true

echo "✅ Cleanup complete!"
