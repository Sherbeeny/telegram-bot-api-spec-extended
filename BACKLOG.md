# Project Backlog

This document tracks planned tasks, features, and bug fixes for the project. It is organized by priority, with the most critical items at the top.

## High Priority

- **Enhance the Scraper:**
    - Add functionality to the scraper to specifically target and extract information from `https://core.telegram.org/bots/faq` and `https://core.telegram.org/bots/features`.
    - Ensure the `ref` key is correctly implemented for all scraped data, including the source URL, anchor, and highlighted text.

## Medium Priority

- **Implement Timestamp Logic:**
    - Add the logic to `update_extensions.py` to correctly manage the `x-last-check` and `x-last-edit` timestamps in the generated JSON files.
- **Implement the Merging Logic:**
    - Create a new script or add to an existing one the functionality to merge the generated `extensions.json` with `api.json` to produce `spec-extended.json`.

## Low Priority

- **Refine the AI Component:**
    - Enhance the AI component to more actively assist in identifying and structuring new information from the scraped text, going beyond just suggesting a general structure.

## Ideas & Future Work

- *(No ideas recorded at the moment)*
