import boto3

client = boto3.client("bedrock", region_name="us-east-1")

response = client.list_foundation_models()

for model in response["modelSummaries"]:
    if "claude" in model["modelId"].lower():
        print(model["modelId"])
