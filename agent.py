from strands import Agent
from strands.models import BedrockModel
import boto3


# Bedrock
bedrock_model = BedrockModel(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    # model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    # model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0.3,
    boto_session=boto3.Session(profile_name="default", region_name="us-east-1"),
    # region="us-east-1",
)

agent = Agent(
    model=bedrock_model,
)

try:
    response = agent("Strandsってどういう意味？")
    print(response)
except Exception as e:
    print(e)
