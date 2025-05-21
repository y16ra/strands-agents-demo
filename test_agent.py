import pytest
import argparse
from agent import parse_arguments, create_agent
from unittest.mock import patch, MagicMock
from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator, http_request, current_time

# Existing tests for parse_arguments

def test_parse_arguments_prompt_only():
    """Tests parsing only the required prompt argument."""
    test_args = ['agent.py', 'Test prompt']
    with patch('sys.argv', test_args):
        args = parse_arguments()
        assert args.prompt == 'Test prompt'
        assert args.model_id == "anthropic.claude-3-5-sonnet-20240620-v1:0"
        assert args.temperature == 0.3
        assert args.profile == "default"
        assert args.region == "us-east-1"

def test_parse_arguments_all_provided():
    """Tests parsing all arguments when provided."""
    test_args = [
        'agent.py',
        'Another test prompt',
        '--model-id', 'custom-model',
        '--temperature', '0.7',
        '--profile', 'custom-profile',
        '--region', 'us-west-2'
    ]
    with patch('sys.argv', test_args):
        args = parse_arguments()
        assert args.prompt == 'Another test prompt'
        assert args.model_id == 'custom-model'
        assert args.temperature == 0.7
        assert args.profile == 'custom-profile'
        assert args.region == 'us-west-2'

def test_parse_arguments_mixed_defaults_and_provided():
    """Tests parsing with a mix of default and provided arguments."""
    test_args = [
        'agent.py',
        'Mixed test prompt',
        '--model-id', 'another-custom-model',
        '--temperature', '0.5'
    ]
    with patch('sys.argv', test_args):
        args = parse_arguments()
        assert args.prompt == 'Mixed test prompt'
        assert args.model_id == 'another-custom-model'
        assert args.temperature == 0.5
        assert args.profile == "default"  # Default
        assert args.region == "us-east-1"  # Default

def test_parse_arguments_temperature_float():
    """Tests that temperature is correctly parsed as a float."""
    test_args = ['agent.py', 'Temp test', '--temperature', '0.9']
    with patch('sys.argv', test_args):
        args = parse_arguments()
        assert args.prompt == 'Temp test'
        assert isinstance(args.temperature, float)
        assert args.temperature == 0.9

def test_parse_arguments_missing_prompt():
    """Tests that argparse raises an error if the prompt is missing."""
    test_args = ['agent.py', '--model-id', 'test-model']
    with patch('sys.argv', test_args):
        with pytest.raises(SystemExit): # argparse exits on error
            parse_arguments()

# New tests for create_agent

@patch('agent.BedrockModel')
@patch('agent.boto3.Session')
def test_create_agent_initialization_defaults(mock_boto_session, mock_bedrock_model_class):
    """Tests create_agent with default profile and region."""
    mock_session_instance = MagicMock()
    mock_boto_session.return_value = mock_session_instance

    mock_bedrock_model_instance = MagicMock()
    mock_bedrock_model_class.return_value = mock_bedrock_model_instance

    agent_instance = create_agent(model_id="test-model-id", temperature=0.5)

    mock_boto_session.assert_called_once_with(profile_name="default", region_name="us-east-1")
    mock_bedrock_model_class.assert_called_once_with(
        model_id="test-model-id",
        temperature=0.5,
        boto_session=mock_session_instance
    )
    assert isinstance(agent_instance, Agent)
    assert agent_instance.model == mock_bedrock_model_instance
    assert agent_instance.tool is not None

@patch('agent.BedrockModel')
@patch('agent.boto3.Session')
def test_create_agent_initialization_custom_params(mock_boto_session, mock_bedrock_model_class):
    """Tests create_agent with custom model_id, temperature, profile, and region."""
    mock_session_instance = MagicMock()
    mock_boto_session.return_value = mock_session_instance

    mock_bedrock_model_instance = MagicMock()
    mock_bedrock_model_class.return_value = mock_bedrock_model_instance
    
    expected_tools = [calculator, http_request, current_time]

    # Call the function to be tested
    agent_instance = create_agent(
        model_id="custom-claude-model",
        temperature=0.7,
        profile_name="dev-profile",
        region_name="eu-west-1"
    )

    # Assertions
    mock_boto_session.assert_called_once_with(profile_name="dev-profile", region_name="eu-west-1")
    mock_bedrock_model_class.assert_called_once_with(
        model_id="custom-claude-model",
        temperature=0.7,
        boto_session=mock_session_instance
    )
    assert isinstance(agent_instance, Agent)
    assert agent_instance.model == mock_bedrock_model_instance
    assert agent_instance.tool is not None

@patch('agent.BedrockModel')
@patch('agent.boto3.Session')
def test_create_agent_uses_passed_tools(mock_boto_session, mock_bedrock_model_class):
    """
    Tests that the Agent is initialized with the correct BedrockModel instance
    and the predefined list of tools.
    """
    # Setup mocks
    mock_session_instance = MagicMock()
    mock_boto_session.return_value = mock_session_instance

    mock_bedrock_model_instance = MagicMock()
    mock_bedrock_model_class.return_value = mock_bedrock_model_instance

    # Expected tools
    expected_tools = [calculator, http_request, current_time]

    # Patch Agent to check its constructor arguments
    with patch('agent.Agent') as mock_agent_class:
        mock_agent_instance = MagicMock()
        mock_agent_class.return_value = mock_agent_instance

        # Call the function
        returned_agent = create_agent(
            model_id="any-model",
            temperature=0.1,
            profile_name="any-profile",
            region_name="any-region"
        )

        # Verify BedrockModel was called (already covered but good for completeness)
        mock_bedrock_model_class.assert_called_once_with(
            model_id="any-model",
            temperature=0.1,
            boto_session=mock_session_instance
        )
        
        # Verify Agent was called with the correct model and tools
        mock_agent_class.assert_called_once_with(
            model=mock_bedrock_model_instance,
            tools=expected_tools
        )
        assert returned_agent == mock_agent_instance

# It's good practice to also test the Agent class directly if it were more complex,
# but here we're focusing on create_agent's orchestration.
# The Agent class itself would have its own unit tests.
# Similarly for BedrockModel.
# boto3.Session is an external library, so we mock it.
# The tools are also imported, and we trust they are correct.
# If the tools list was dynamic, we'd test that logic.
# Here, it's a fixed list.
