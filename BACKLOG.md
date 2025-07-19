# Project Backlog

This document tracks planned tasks, features, and bug fixes for the project. It is organized by priority, with the most critical items at the top.

## High Priority

- **Implement Timestamp Logic:**
    - Add the logic to `update_extensions.py` to correctly manage the `x-last-check` and `x-last-edit` timestamps in the generated JSON files.
- **Implement the Merging Logic:**
    - Create a new script or add to an existing one the functionality to merge the generated `extensions.json` with `api.json` to produce `spec-extended.json`.

## Medium Priority

- **Refine the AI Component:**
    - Enhance the AI component to more actively assist in identifying and structuring new information from the scraped text, going beyond just suggesting a general structure.
    - Ensure the AI output is deterministic.
    - Ensure the AI intelligently updates existing entries rather than creating new ones.

## Low Priority

- **Expand Scraper to Community Sources:**
    - Add functionality to the scraper to incorporate information from community sources and experiments.
- **Add Documentation-Specific Fields:**
    - Implement logic to include fields like `x-notes`, `x-simulated-behavior`, and `x-likely-side-effects` in the generated JSON.
- **Ensure Valid OpenAPI Extensions:**
    - Add validation to ensure all extra data is formatted as valid OpenAPI extensions.
- **Implement Comprehensive Data Categories:**
    - Expand the scraper and data processing to extract and categorize a wide range of information, including rate limits, tier access, webhook behavior, restrictions, and error handling.


## Completed

- **Enhance the Scraper:**
    - Added functionality to the scraper to specifically target and extract information from `https://core.telegram.org/bots/faq` and `https://core.telegram.org/bots/features`.
    - Ensured the `ref` key is correctly implemented for all scraped data, including the source URL, anchor, and highlighted text.

## Ideas & Future Work

- *(No ideas recorded at the moment)*
