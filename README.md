# AI Agent Tester


![Python](https://img.shields.io/badge/python-3.10+-blue.svg)  ![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)  ![HTTPX](https://img.shields.io/badge/httpx-0.27.0-blue)   ![NLTK](https://img.shields.io/badge/nltk-3.8.1-blue) ![License](https://img.shields.io/badge/License-MIT-yellow.svg)


A simple application for testing an AI Agent by sending multiple prompts and validating the responses based on expected keywords.

## 🎯 Objective

The main objective of this application is to automate the testing process of an AI Agent (such as OpenAI's GPT). The script reads a list of prompts from a CSV file, sends each prompt to the OpenAI API, and checks if the response contains a specific keyword. At the end, a detailed report in JSON format is generated with the result of each test (Success or Failure).

## ⚙️ How It Works

The application execution flow is as follows:

```mermaid
sequenceDiagram
participant User as User
participant main.py as Main Script
participant prompts.csv as Prompts File
participant OpenAI_API as OpenAI API
participant report.log as Report File

User->>main.py: Run `python main.py`
main.py->>prompts.csv: Load the prompts and keywords
loop For each prompt in the CSV
main.py->>OpenAI_API: Send the prompt to the model
OpenAI_API-->>main.py: Return the AI response
main.py->>main.py: Validate if the response contains the keyword
main.py->>report.log: Add the result to the report
end
main.py->>report.log: Save the final report in JSON format
main.py-->>User: Displays "Testing complete"
```

## 🚀 Getting Started

Follow the steps below to set up and run the project.

### Prerequisites

- Python 3.10 or higher
- An OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <YOUR_REPOSITORY_URL>
cd agent_test
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI key:
```
OPENAI_API_KEY="your_secret_key_here"
```

### Setting Up the Tests

Edit the `prompts.csv` file to add the prompts you want to test. Each line must contain a `prompt` and the `target_word` (expected keyword in the response).

```csv
prompt,target_word
"What is the capital of France?","Paris"
"Describe the sun.","star"
```

### Execution

To run the tests, execute the main script:
```bash
python main.py
```

At the end of the execution, a `report.log` file will be created in the project root with detailed results.

## 🧪 Running the Tests

To run the project's automated test suite, use the following command:
```bash
python -m unittest discover tests
```

## 🤝 Contributing

Contributions are welcome! Please read our contributing guide to understand our code guidelines and submission process.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
