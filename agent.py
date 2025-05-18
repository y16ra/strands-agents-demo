import argparse
from strands import Agent
from strands.models import BedrockModel
import boto3
from strands_tools import calculator, http_request, current_time

def create_agent(model_id, temperature=0.3, profile_name="default", region_name="us-east-1"):
    """エージェントを作成する
    
    Args:
        model_id (str): 使用するモデルID
        temperature (float): モデルの温度パラメータ (0.0-1.0)
        profile_name (str): AWSプロファイル名
        region_name (str): AWSリージョン名
    """
    bedrock_model = BedrockModel(
        model_id=model_id,
        temperature=temperature,
        boto_session=boto3.Session(profile_name=profile_name, region_name=region_name),
    )
    return Agent(
        model=bedrock_model,
        tools=[calculator, http_request, current_time],
    )

def parse_arguments():
    """コマンドライン引数をパースする"""
    parser = argparse.ArgumentParser(description='Agent を実行します')
    parser.add_argument('prompt', type=str, help='エージェントに送信するプロンプト')
    parser.add_argument('--model-id', type=str, 
                        default="anthropic.claude-3-5-sonnet-20240620-v1:0",
                        help='使用するモデルID')
    parser.add_argument('--temperature', type=float, default=0.3,
                        help='モデルの温度パラメータ (0.0-1.0)')
    parser.add_argument('--profile', type=str, default="default",
                        help='AWSプロファイル名')
    parser.add_argument('--region', type=str, default="us-east-1",
                        help='AWSリージョン名')
    return parser.parse_args()

def main():
    """メインエントリーポイント"""
    args = parse_arguments()
    
    try:
        agent = create_agent(
            model_id=args.model_id,
            temperature=args.temperature,
            profile_name=args.profile,
            region_name=args.region
        )
        response = agent(args.prompt)
        print(response)
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
