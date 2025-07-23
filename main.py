import os
import json
import csv
import httpx
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from openai import OpenAI
from dotenv import load_dotenv

# Initialize the stemmer once for efficiency
stemmer = PorterStemmer()

def check_response(response: str, keyword: str) -> bool:
    """
    Checks if the stemmed version of the keyword is present in the tokenized and
    stemmed response. The check is case-insensitive and uses stemming to match
    word roots (e.g., 'flying' matches 'fly').

    Args:
        response: The text response from the AI agent.
        keyword: The word to search for in the response.

    Returns:
        True if the keyword's stem is found, False otherwise.
    """
    # Ensure NLTK 'punkt' tokenizer is available. This is a one-time check.
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("First-time setup: Downloading NLTK 'punkt' model...")
        nltk.download('punkt', quiet=True)
        print("'punkt' model downloaded.")

    # Tokenize the response, then stem each token
    tokens = word_tokenize(response.lower())
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    # Stem the keyword and check for its presence in the stemmed tokens
    stemmed_keyword = stemmer.stem(keyword.lower())
    return stemmed_keyword in stemmed_tokens

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

def write_report(file_path: str, results: list):
    """
    Writes a list of test results to a report file in JSON format.

    Args:
        file_path: The path to the report log file.
        results: A list of dictionaries with test results.
    """
    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(results, f, indent=4)

def run_tests(prompts_file="prompts.csv", report_file="report.log"):
    """
    Main function to run the AI agent testing process. It loads prompts,
    gets AI responses, checks them, and logs the results.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found. Please ensure it is set in the .env file.")
        return
    all_results = []

    try:
        prompts = load_prompts(prompts_file)

        # Configure an httpx client to handle proxy settings from environment variables
        http_client = httpx.Client(
            proxies={
                "http://": os.getenv("HTTP_PROXY"),
                "https://": os.getenv("HTTPS_PROXY"),
            }
        )
        client = OpenAI(api_key=api_key, http_client=http_client)

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
