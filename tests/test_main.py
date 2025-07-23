import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
import os
import sys

# Add the project root to the Python path to allow importing 'main'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the new functions from main
from main import check_response, get_ai_response, load_prompts, run_tests, write_report

class TestAIHelpers(unittest.TestCase):
    """Unit tests for helper functions in main.py."""

    def test_check_response(self):
        """Tests the keyword checking logic."""
        self.assertTrue(check_response("The capital is Paris.", "paris"))
        self.assertFalse(check_response("The capital is Paris.", "berlin"))
        self.assertTrue(check_response("A response about SOLAR power.", "solar"))
        self.assertTrue(check_response("Case-insensitivity test: SuNsEt", "sunset"))

    @patch("builtins.open", new_callable=mock_open, read_data='prompt,target_word\n"Is it sunny?","sun"\n"Is it rainy?","rain"')
    def test_load_prompts(self, mock_file):
        """Tests loading and parsing of the prompts CSV."""
        prompts = load_prompts("fake_path.csv")
        self.assertEqual(len(prompts), 2)
        self.assertEqual(prompts[0], {"prompt": "Is it sunny?", "target_word": "sun"})
        self.assertEqual(prompts[1], {"prompt": "Is it rainy?", "target_word": "rain"})
        mock_file.assert_called_once_with("fake_path.csv", mode='r', encoding='utf-8')

    def test_get_ai_response(self):
        """
        Tests the get_ai_response function by mocking the OpenAI client.
        This serves as an integration test for the interaction with the client object.
        """
        # Arrange
        mock_client_instance = MagicMock()

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "This is a test response."
        mock_client_instance.chat.completions.create.return_value = mock_completion

        prompt = "This is a test prompt."

        # Act
        response = get_ai_response(mock_client_instance, prompt)

        # Assert
        mock_client_instance.chat.completions.create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        self.assertEqual(response, "This is a test response.")

    @patch("main.json.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_write_report(self, mock_file, mock_json_dump):
        """Tests writing the report to a file."""
        # Arrange
        file_path = "test_report.log"
        results = [{"status": "Success"}]

        # Act
        write_report(file_path, results)

        # Assert
        mock_file.assert_called_once_with(file_path, "w", encoding='utf-8')
        mock_json_dump.assert_called_once_with(results, mock_file(), indent=4)

class TestMainRunner(unittest.TestCase):
    """
    Integration-style tests for the main run_tests function.
    """

    def setUp(self):
        """Set up for tests."""
        self.report_file = "test_report.log"
        if os.path.exists(self.report_file):
            os.remove(self.report_file)

    def tearDown(self):
        """Tear down after tests."""
        if os.path.exists(self.report_file):
            os.remove(self.report_file)

    @patch('main.os.getenv')
    @patch('main.load_prompts')
    @patch('main.httpx.Client')
    @patch('main.OpenAI')
    @patch('main.write_report')
    def test_run_tests_e2e_mocked(self, mock_write_report, mock_openai, mock_httpx_client, mock_load_prompts, mock_getenv):
        """
        Tests the main run_tests function with mocked dependencies, including client initialization.
        """
        # Arrange
        # Mock environment variables for API key and proxy
        def getenv_side_effect(key, default=None):
            return {
                "OPENAI_API_KEY": "fake_api_key",
                "HTTP_PROXY": "http://proxy.example.com:8080",
                "HTTPS_PROXY": "https://proxy.example.com:8080",
            }.get(key, default)
        mock_getenv.side_effect = getenv_side_effect

        # Mock file loading
        mock_load_prompts.return_value = [
            {"prompt": "What is the capital of France?", "target_word": "Paris"},
            {"prompt": "What is a star?", "target_word": "gas"}
        ]

        # Mock the httpx and OpenAI clients
        mock_httpx_instance = MagicMock()
        mock_httpx_client.return_value = mock_httpx_instance

        mock_openai_instance = MagicMock()
        mock_openai.return_value = mock_openai_instance

        # Mock the response from the get_ai_response function's internal call
        mock_completion_1 = MagicMock()
        mock_completion_1.choices[0].message.content = "The capital of France is indeed Paris."
        mock_completion_2 = MagicMock()
        mock_completion_2.choices[0].message.content = "A star is a luminous ball of plasma."
        mock_openai_instance.chat.completions.create.side_effect = [mock_completion_1, mock_completion_2]

        # Act
        run_tests(report_file=self.report_file)

        # Assert
        # Verify client initialization
        mock_httpx_client.assert_called_once_with(
            proxies={
                "http://": "http://proxy.example.com:8080",
                "https://": "https://proxy.example.com:8080",
            }
        )
        mock_openai.assert_called_once_with(api_key="fake_api_key", http_client=mock_httpx_instance)

        # Verify main logic
        mock_load_prompts.assert_called_once_with("prompts.csv")
        self.assertEqual(mock_openai_instance.chat.completions.create.call_count, 2)

        # Verify report writing
        mock_write_report.assert_called_once()
        call_args = mock_write_report.call_args[0]
        self.assertEqual(call_args[0], self.report_file)
        actual_results = call_args[1]
        expected_results = [
            {
                'prompt': 'What is the capital of France?',
                'expected_keyword': 'Paris',
                'response': 'The capital of France is indeed Paris.',
                'status': 'Success'
            },
            {
                'prompt': 'What is a star?',
                'expected_keyword': 'gas',
                'response': 'A star is a luminous ball of plasma.',
                'status': 'Fail'
            }
        ]
        self.assertEqual(actual_results, expected_results)
