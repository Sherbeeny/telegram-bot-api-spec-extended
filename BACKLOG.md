# Project Backlog

This document tracks planned tasks, features, and bug fixes for the project. It is organized by priority, with the most critical items at the top.

## High Priority

- **Enhance the Scraper:**
    - Add functionality to the scraper to specifically target and extract information from `https://core.telegram.org/bots/faq` and `https://core.telegram.org/bots/features`.
    - Ensure the `ref` key is correctly implemented for all scraped data, including the source URL, anchor, and highlighted text.
- **Refactor Scraper and Add AI Component:** **(DONE)**
    - Refactor the scraper to first load and analyze `api.json` to avoid duplicating information.
    - Introduce a basic AI component to help structure the scraped data and ensure consistency with the existing spec.

## Medium Priority

- **Implement the Merging Logic:**
    - Create a new script or add to an existing one the functionality to merge the generated `extensions.json` with `api.json` to produce `spec-extended.json`.
- **Fix GitHub Actions Workflow:** **(DONE)**
    - The GitHub Actions workflow for `update_extensions.py` was failing due to missing dependencies. This has been fixed by installing dependencies from `requirements.txt`.

## Low Priority

- **Refine the AI Component:**
    - Enhance the AI component to more actively assist in identifying and structuring new information from the scraped text, going beyond just suggesting a general structure.
- **Implement Timestamp Logic:** **(DONE)**
    - Add the logic to `update_extensions.py` to correctly manage the `x-last-check` and `x-last-edit` timestamps in the generated JSON files.

## Ideas & Future Work

- *(No ideas recorded at the moment)*
