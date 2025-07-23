# Contributing to the AI Agent Tester

First off, thank you for considering contributing to this project! Your help is greatly appreciated. Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

## Project Context

This application is designed to test an AI Agent. The core functionality involves:

1.  Sending a series of predefined prompts to an AI endpoint.
2.  Receiving the responses from the AI Agent.
3.  Analyzing each response to verify the presence of a specific keyword or phrase.
4.  Generating a comprehensive report (e.g., `report.log` in the root directory) that logs each prompt, its response, and whether the test passed (`Success`) or failed (`Fail`).

## Contribution Rules

To ensure the project remains maintainable, scalable, and of high quality, please adhere to the following rules when contributing.

### 1. Response Handling

All responses from the AI endpoint must be stored. Each response needs to be reviewed to check for the expected word, and the result must be clearly marked as "Success" or "Fail" in the final report.

### 2. Code Documentation

Every function, method, or significant operation you create must include a simple documentation comment (e.g., Javadoc, TSDoc, docstrings) explaining its purpose, parameters, and what it returns.

**Example (Python):**
```python
# TODO: Create a unit test for this function.
def check_response(response: str, keyword: str) -> bool:
    """
    Checks if the keyword is present in the AI's response.

    Args:
        response: The text response from the AI agent.
        keyword: The word to search for in the response.

    Returns:
        True if the keyword is found, False otherwise.
    """
    return keyword.lower() in response.lower()
```

### 3. SOLID and Best Practices

Your code should always follow the SOLID principles and other modern software development best practices. This includes writing clean, readable, and maintainable code.

### 4. Performance First

Before you start writing code for a new feature or fix, take a moment to consider the performance implications of your chosen approach. We strive for efficient solutions, so please evaluate if there's a more performant way to achieve the goal.

### 5. Testing is Key

For every new piece of logic (function, method, class), you must add a `TODO` comment indicating that a test is needed. This serves as a reminder to create a corresponding unit or integration test.

**Examples:**
`# TODO: Create a unit test for the report generation logic.`
`// TODO: Create an integration test for the AI endpoint communication.`

### 6. Simplicity and Design Patterns

Keep your solutions as simple and straightforward as possible. While Design Patterns are powerful, they should only be used when they provide a clear and significant benefit to the application's structure, maintainability, or scalability. Avoid over-engineering.
