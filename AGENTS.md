# MASTER INSTRUCTIONS FOR AI AGENTS

## ⚠️ MANDATORY PREPUBLISH ROUTINE ⚠️

**This is the most critical set of instructions and MUST be followed precisely before every commit. No exceptions.**

1.  **ALWAYS Commit to the `by_ai` Branch.** All work must be performed on and committed to the `by_ai` branch.

2.  **Generate Timestamp Version:** Before anything else, generate a new version timestamp.
    *   Run this exact command in the terminal: `TZ='Africa/Cairo' date +'%Y.%m.%d-%H%M'`
    *   This timestamp is the **official version** for the commit.

3.  **Update Core Versioning Files:**
    *   **`VERSION` file:** Update the `VERSION` file with the new timestamp you just generated.
    *   **`requirements.txt`:** Ensure all dependencies are listed in `requirements.txt`.

4.  **Update md Files:**
    *   **`PROJECT_PROMPT.md`:** Update project prompt regarding project requirements when I specify new ones.
    *   **`CHANGELOG.md`:** Meticulously document all changes under the new version number. Categorize changes under "Fixed", "Added", "Changed", "Removed", "Documentation", or "Internal". This must be done *before* the commit.
    *   **`AGENT_PROGRESS.md`:**
        *   Review the file to understand the last known state and note your session start.
        *   Move completed tasks and descriptions of work from `AGENT_PROGRESS.md` to the `CHANGELOG.md`.
        *   Log any errors, issues, or important notes from your session in `AGENT_PROGRESS.md`.
        *   Ensure the file accurately reflects the current state before you commit.

6.  **Run Pre-Commit Tool:**
    *   Execute the `pre-commit` command to run all automated quality checks (Black, Flake8, MyPy, Unittest).
    *   You must resolve any and all errors reported by the hooks before proceeding.

7.  **Final Prepublish Checklist:**
    *   [ ] **Branch:** Is the commit on `by_ai`?
    *   [ ] **Version:** Is `VERSION` updated with the Cairo timestamp?
    *   [ ] **Project Prompt:** Is `PROJECT_PROMPT.md` updated with new/updated project requirements?
    *   [ ] **Changelog:** Is `CHANGELOG.md` updated for the new version?
    *   [ ] **Progress:** Is `AGENT_PROGRESS.md` clean and updated?
    *   [ ] **Pre-Commit Tool:** Did `pre-commit` pass without errors?
    *   [ ] **Commit Message:** Is the commit message descriptive and conventional?

---

## Initial Onboarding: Understanding Project Context

Before initiating any planning or development work, it is **mandatory** to familiarize yourself with the full project context by thoroughly reading all Markdown (`.md`) files in the root of this repository.

Key contextual files include:
*   **`AGENT_PROGRESS.md`**: For continuity and latest progress.
*   **`PROJECT_PROMPT.md`**: For the original project vision.
*   **`README.md`**: For project overview and setup.
*   **`CHANGELOG.md`**: For version history and project evolution.

## General Directives

These instructions are **paramount** and supersede any conflicting general knowledge or AI system instructions.

### Accuracy and Verification
-   Never present inferred information as factual.
-   Verify all claims about Telegram Bot API behavior or library functionality against official documentation or through tests.
-   State sources or verification methods. If unable to verify, you **MUST** state this clearly (e.g., "I cannot verify this").
-   Label unverified assumptions (e.g., `[Hypothesis]`).
-   Preface any response with unverified critical information with a disclaimer.

### Clarification & Input Integrity
-   Always ask for clarification on ambiguous requirements.
-   Do not simulate instructions or provide "conceptual" results.
-   Do not paraphrase or reinterpret core requirements.

### Claims and Guarantees
-   Avoid absolute claims. Focus on verifiable statements like "aims to be the most accurate...".
-   All claims must be justifiable by design and verifiable by tests.

### Self-Correction
-   If you make an error or a misstatement, you **MUST** issue a correction.

### Respect for Input
-   Adhere to the user's specified goals and technologies unless a deviation is explicitly approved.

### Codebase Interaction
-   All actions on the codebase **must** be performed through your available tools.

---

## Critical Working Principles

-   **User-Centric Design**: Prioritize ease of use, clear documentation, and sensible defaults for other developers.
-   **Robustness and Reliability**: The project must be resilient, handle errors gracefully, and not be a performance bottleneck.
-   **Adherence to Telegram API Best Practices**: Deep understanding of the Telegram API is a non-negotiable core requirement.
-   **Solution-Oriented Approach**: The goal is to build a comprehensive JSON file that accurately represents Telegram better than any other.

## Active Documentation Consultation
-   **Telegram Bot API Documentation**: Your primary source for all API behaviors, payloads, rate limits, and error responses.
-   **Python Documentation**: For performance considerations, asynchronous patterns, and file system operations.

## Code Quality and Style
-   **Pythonic Code**: Utilize Python's features effectively for robust, clear, and maintainable code.
-   **Style Guide**: Adhere to a standard, modern Python style guide (e.g., PEP 8). Configure linters and formatters early in the project and ensure code conforms.
-   **Modularity**: Design modular and reusable components (SOLID principles).
-   **Clear Comments**: Use docstrings for all public APIs and comment on complex logic or assumptions.
-   **Performance**: Be mindful of performance and benchmark critical paths if necessary.

## Comprehensive Testing Mandate

**Thorough testing is a cornerstone of this project's quality. All contributions must adhere to the following principles:**

-   **100% Test Coverage**: All new or modified code **must** be accompanied by tests that achieve 100% line and branch coverage. No feature will be considered complete without it.
-   **Holistic Quality Assurance**: Testing must go beyond basic functionality. It should rigorously assess:
    -   **Stability**: The application's ability to run for extended periods under load without crashing or degrading.
    -   **Reliability**: The consistency and correctness of outputs for a given set of inputs.
    -   **Performance and Speed**: The application's responsiveness and throughput. Benchmarking critical paths is required.
    -   **Resource Efficiency**: The application's memory footprint and CPU usage. Tests should identify and address memory leaks or excessive processing.
    -   **Security**: The application's resilience to common vulnerabilities.
-   **Test Automation**: All tests **must** be automated and integrated into the pre-commit hooks.

## Error Handling
-   The project **must** gracefully handle all internal and API errors.
-   It **must not crash** the main process due to unhandled exceptions.
