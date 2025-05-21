import boto3

def print_claude_models():
    """
    Creates a Bedrock client, lists foundation models, and prints the model IDs
    of those containing "claude" (case-insensitive).
    """
    client = boto3.client("bedrock", region_name="us-east-1")
    response = client.list_foundation_models()

    for model in response["modelSummaries"]:
        if "claude" in model["modelId"].lower():
            print(model["modelId"])

if __name__ == "__main__":
    print_claude_models()
