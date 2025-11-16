#!/bin/sh
# Setup Git hooks for this repository
# This configures Git to use .githooks directory for hooks

set -e

echo "Setting up Git hooks..."
git config core.hooksPath .githooks
echo "✓ Git hooks configured successfully!"
echo ""
echo "Git will now use hooks from .githooks directory"
echo "Pre-commit hook will automatically sanitize sensitive data"
