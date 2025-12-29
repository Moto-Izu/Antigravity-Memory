#!/bin/bash

# Flight Log Generator for Antigravity
# Usage: ./scripts/log_flight.sh

LOG_DIR="logs"
TODAY=$(date +%Y-%m-%d)
LOG_FILE="${LOG_DIR}/${TODAY}_flight_log.md"

if [ ! -f "$LOG_FILE" ]; then
    echo "Creating new Flight Log for $TODAY..."
    cat <<EOF > "$LOG_FILE"
# ✈️ Antigravity Flight Log: $TODAY

## 🎯 Daily Mission
- [ ] 

## 📝 Activity Log
| Time | Action | Outcome |
| :--- | :--- | :--- |
| $(date +%H:%M) | **System Start** | Verified YOROZU Environment |

## 🧠 Key Decisions & Insights
- 

## 🔗 NotebookLM Source
*(Paste this content into NotebookLM for reflection)*
EOF
    echo "Flight Log initialized: $LOG_FILE"
else
    echo "Flight Log already exists: $LOG_FILE"
fi

# Open the log file for viewing/editing (Optional - you can use 'code' if available)
# code "$LOG_FILE"
