#!/bin/bash

# This script is the entry point for the prepublish routine.
# It performs automated checks and then hands off to the manual checklist chain.

# --- Automated Tasks ---

echo "Running automated tasks..."

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

# --- Handoff to Manual Checklist ---

echo "--------------------------------------------------"
if [ $HOOK_STATUS -ne 0 ]; then
    echo "⚠️ Pre-commit hooks failed. Please review the errors above."
    echo "You can choose to proceed to document the failure and commit the work-in-progress."
else
    echo "✅ Pre-commit hooks passed successfully."
fi
echo "--------------------------------------------------"
echo "Automated tasks complete."
echo "Now, begin the manual checklist by running the following command:"
echo ""
echo "    ./scripts/1_readme_check.sh"
echo ""
