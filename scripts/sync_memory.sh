#!/bin/bash

# Memory Sync for Antigravity
# Usage: ./scripts/sync_memory.sh [commit_message]

# Check if a commit message was provided
if [ -z "$1" ]; then
    COMMIT_MSG="🧠 Sync Memory: $(date +%Y-%m-%d\ %H:%M)"
else
    COMMIT_MSG="🧠 $1"
fi

echo "Initiating Memory Sync..."

# Add all changes (Workflows, Rules, Logs)
git add .agent assets logs scripts

# Commit
git commit -m "$COMMIT_MSG"

# Pull latest changes (rebase to keep history clean)
echo "Pulling latest memory..."
git pull --rebase origin main

# Push (assumes remote 'origin' is set)
echo "Pushing to remote..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Memory successfully synchronized!"
else
    echo "⚠️ Push failed. Please check remote configuration."
fi
