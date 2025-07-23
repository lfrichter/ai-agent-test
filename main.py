import os
import json
import csv
from openai import OpenAI
from dotenv import load_dotenv

# TODO: Create a unit test for this function.
def check_response(response: str, keyword: str) -> bool:
    """
    Checks if the keyword is present in the AI's response (case-insensitive).

    Args:
        response: The text response from the AI agent.
        keyword: The word to search for in the response.

    Returns:
        True if the keyword is found, False otherwise.
    """
    return keyword.lower() in response.lower()

# TODO: Create an integration test for this function.
def get_ai_response(client: OpenAI, prompt: str) -> str:
    """
    Sends a prompt to the OpenAI API and returns the response content.

    Args:
        client: An initialized OpenAI client instance.
        prompt: The user prompt to send to the AI.

    Returns:
        The content of the AI's response as a string.
    """
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

# TODO: Create a unit test for this function.
def load_prompts(file_path: str) -> list:
    """
    Loads prompts and target keywords from a CSV file.

    Args:
        file_path: The path to the CSV file.

    Returns:
        A list of dictionaries, each containing a 'prompt' and 'target_word'.
    """
    prompts = []
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            prompts.append(row)
    return prompts

# TODO: Create a unit test for this function.
def write_report(file_path: str, results: list):
    """
    Writes a list of test results to a report file in JSON format.

    Args:
        file_path: The path to the report log file.
        results: A list of dictionaries with test results.
    """
    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(results, f, indent=4)

def run_tests():
    """
    Main function to run the AI agent testing process. It loads prompts,
    gets AI responses, checks them, and logs the results.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found. Please ensure it is set in the .env file.")
        return

    prompts_file = "prompts.csv"
    report_file = "report.log"
    all_results = []

    try:
        prompts = load_prompts(prompts_file)
        client = OpenAI(api_key=api_key)

        for item in prompts:
            prompt = item['prompt']
            keyword = item['target_word']
            print(f"Testing prompt: '{prompt}'")
            response_content = get_ai_response(client, prompt)
            is_success = check_response(response_content, keyword)

            all_results.append({
                "prompt": prompt,
                "expected_keyword": keyword,
                "response": response_content,
                "status": "Success" if is_success else "Fail"
            })

        write_report(report_file, all_results)
        print(f"\nTesting complete. Full report saved to {report_file}")

    except FileNotFoundError:
        print(f"Error: The prompts file '{prompts_file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_tests()
