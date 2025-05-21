import unittest
from unittest.mock import patch, MagicMock
import io
import contextlib
# import runpy # No longer needed
# import sys # No longer needed
from get_models import print_claude_models # Import the function

class TestGetModelsScript(unittest.TestCase):

    @patch('get_models.boto3.client')  # Patch the boto3.client used within get_models.py
    def test_get_models_filters_claude(self, mock_boto_client_function):
        # mock_boto_client_function is the mock for the boto3.client function
        mock_bedrock_instance = MagicMock()
        mock_boto_client_function.return_value = mock_bedrock_instance

        mock_response = {
            "modelSummaries": [
                {"modelId": "anthropic.claude-v2", "modelName": "Claude V2"},
                {"modelId": "anthropic.claude-instant-v1", "modelName": "Claude Instant V1"},
                {"modelId": "amazon.titan-text-lite-v1", "modelName": "Titan Text Lite"},
                {"modelId": "anthropic.claude-3-sonnet-20240229-v1:0", "modelName": "Claude 3 Sonnet"},
            ]
        }
        mock_bedrock_instance.list_foundation_models.return_value = mock_response

        stdout_capture = io.StringIO()
        with contextlib.redirect_stdout(stdout_capture):
            print_claude_models() # Call the function directly

        captured_output = stdout_capture.getvalue()
        expected_output_lines = [
            "anthropic.claude-v2",
            "anthropic.claude-instant-v1",
            "anthropic.claude-3-sonnet-20240229-v1:0",
        ]
        actual_output_lines = captured_output.strip().split('\n')
        
        if not captured_output.strip(): # Handle empty output case
            actual_output_lines = []

        self.assertEqual(len(actual_output_lines), len(expected_output_lines), f"Output lines mismatch. Expected {len(expected_output_lines)}, Got: {len(actual_output_lines)}. Output:\n{captured_output}")
        for line in expected_output_lines:
            self.assertIn(line, actual_output_lines, f"Expected line '{line}' not found in output:\n{captured_output}")
        
        # Check that the non-Claude model (if present in mock_response) is not in the output
        is_non_claude_in_mock = any(
            "amazon.titan-text-lite-v1" in model["modelId"] for model in mock_response["modelSummaries"]
        )
        if is_non_claude_in_mock:
             self.assertNotIn("amazon.titan-text-lite-v1", captured_output, f"Non-claude model 'amazon.titan-text-lite-v1' found in output:\n{captured_output}")

if __name__ == '__main__':
    unittest.main()
