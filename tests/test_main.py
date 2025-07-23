import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
import os
import sys

# Add the project root to the Python path to allow importing 'main'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the new functions from main
from main import check_response, load_prompts, run_tests

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

class TestMainRunner(unittest.TestCase):
    """
    Integration-style tests for the main run_tests function.
    """

    def setUp(self):
        """Set up for tests."""
        self.report_file = "report.log"
        if os.path.exists(self.report_file):
            os.remove(self.report_file)

    def tearDown(self):
        """Tear down after tests."""
        if os.path.exists(self.report_file):
            os.remove(self.report_file)

    @patch('main.os.getenv')
    @patch('main.load_prompts')
    @patch('main.get_ai_response')
    @patch('main.write_report')
    def test_run_tests_e2e_mocked(self, mock_write_report, mock_get_ai_response, mock_load_prompts, mock_getenv):
        """
        Tests the main run_tests function with mocked dependencies.
        """
        # Arrange
        mock_getenv.return_value = "fake_api_key"
        mock_load_prompts.return_value = [
            {"prompt": "What is the capital of France?", "target_word": "Paris"},
            {"prompt": "What is a star?", "target_word": "gas"}
        ]
        # Make get_ai_response return different values on subsequent calls
        mock_get_ai_response.side_effect = [
            "The capital of France is indeed Paris.",
            "A star is a luminous ball of plasma." # This response fails the check
        ]

        # Act
        run_tests()

        # Assert: Verify the outcomes
        mock_load_prompts.assert_called_once_with("prompts.csv")
        self.assertEqual(mock_get_ai_response.call_count, 2)

        # Check the data that write_report would have been called with
        mock_write_report.assert_called_once()
        actual_results = mock_write_report.call_args[0][1]

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
