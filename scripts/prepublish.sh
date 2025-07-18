#!/bin/bash

# This script automates the prepublish routine, running automated checks before the manual checklist.

# --- Automated Tasks ---

# Generate timestamp version
TIMESTAMP=$(TZ='Africa/Cairo' date +'%Y.%m.%d-%H%M')
echo "Generated version: $TIMESTAMP"

# Update VERSION file
echo $TIMESTAMP > VERSION
echo "Updated VERSION file."

# Run pre-commit hooks
echo "Running pre-commit hooks..."
pre-commit run --all-files
HOOK_STATUS=$? # Capture the exit status of the pre-commit hooks

# Update requirements.txt
echo "Updating requirements.txt..."
pip freeze > requirements.txt

# --- Interactive Checklist ---

# Only proceed to the checklist if the user decides to, based on the hook status
echo "--------------------------------------------------"
if [ $HOOK_STATUS -ne 0 ]; then
    echo "⚠️ Pre-commit hooks failed. Please review the errors above."
    echo "You can choose to proceed to document the failure and commit the work-in-progress."
else
    echo "✅ Pre-commit hooks passed successfully."
fi
echo "--------------------------------------------------"


echo "Please confirm the following manual documentation steps have been completed:"

# Function to ask a question and wait for a valid response
ask_question() {
    while true; do
        read -p "$1 (yes/no/not needed): " answer
        case $answer in
            [Yy]es) return 0;;
            [Nn]o) echo "Please complete the task and try again.";;
            [Nn]ot\ needed) return 0;;
            *) echo "Invalid response. Please answer with 'yes', 'no', or 'not needed'.";;
        esac
    done
}

ask_question "Have you refreshed your context by re-reading the relevant .md files and the session plan?"
ask_question "Is the commit on the 'by_ai' branch?"
ask_question "Is the BACKLOG.md updated (e.g., task moved to 'In Progress' or 'Done')?"
ask_question "Is the CHANGELOG.md updated (if task is complete)?"
ask_question "Is AGENT_PROGRESS.md updated with the latest progress or details of any hook failures?"
ask_question "Is the PROJECT_PROMPT.md updated with new/updated project requirements?"

echo "Prepublish routine complete. Ready to commit."
