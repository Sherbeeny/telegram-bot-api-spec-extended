## [2025.07.18-1509]
### Changed
- Updated `PROJECT_PROMPT.md` to reflect new requirements.
- Updated `scraper.py` to use the `ref` key.
- Updated `update_extensions.py` to use the `ref` key and propose an AI component.
- Updated the GitHub Actions workflow to run weekly.

### Fixed
- Fixed failing tests.

### Internal
- Encountered a corrupted environment and decided to commit the changes and address the pre-commit hook issue in a separate session.

## [2025.07.18-1411]
### Fixed
- The pre-commit hooks now run successfully.
- The `.coverage` file is now correctly generated.

### Internal
- Updated `AGENT_PROGRESS.md` to reflect the latest changes.
- Complied with the pre-commit protocol outlined in `AGENTS.md`.

## [2025.07.18-1257]
### Changed
- Reimplemented the scraper and generator with a more modular and robust architecture.
- The script now generates `extensions.ref.json` with source references.
- The script now generates `extensions.json` and `extensions.min.json` from `extensions.ref.json`.
- The GitHub Actions workflow now runs weekly.
- Added tests for the scraper and generator.

## [2025.07.18-0348]
### Changed
- Updated `PROJECT_PROMPT.md` with new requirements.
- Modified the scraping script to generate `extensions.ref.json`.
- Modified the script to generate `extensions.json` from `extensions.ref.json`.
- Updated the GitHub Actions workflow to run weekly.
- Investigated and proposed an AI component.
- Refined and tested the script.

## [2025.07.18-0322]
### Changed
- Updated `PROJECT_PROMPT.md` to prioritize automation.
- Refactored `scraper.py` to be more robust and comprehensive.
- Updated `update_extensions.py` to use the new scraper and generate `extensions.json` correctly.
- Added tests for `scraper.py` and `update_extensions.py`.

## [2025.07.18-0303]
### Changed
- Updated `extensions.json` with more accurate and detailed information for `sendMessage`, `sendPhoto`, `editMessageText`, `answerCallbackQuery`, and `getUpdates` methods.
- Added `x-restrictions` to document limits for the above methods.
