# Strands Agents デモプロジェクト

このリポジトリは、Strands Agents を使用したデモンストレーション用のプロジェクトです。AWS Bedrock の Claude モデルを利用して、エージェントを簡単に構築・実行するサンプルコードを含んでいます。

## プロジェクト構成

```
.
├── README.md          # このファイル
├── agent.py          # Strands Agent の基本的な使用例
├── get_models.py     # 利用可能なモデルを一覧表示するスクリプト
├── requirements.txt  # 依存パッケージ一覧
└── LICENSE           # ライセンスファイル
```

## セットアップ

1. リポジトリをクローンします:
   ```bash
   git clone https://github.com/y16ra/strands-agents-demo.git
   cd strands-agents-demo
   ```

2. 必要なパッケージをインストールします:
   ```bash
   pip install -r requirements.txt
   ```

3. AWS 認証情報を設定します:
   - `~/.aws/credentials` に適切なプロファイルを設定するか、環境変数で認証情報を設定してください
   - 必要な権限: `bedrock:InvokeModel`, `bedrock:ListFoundationModels`

## 使用方法

### 利用可能なモデルの一覧を表示

```bash
python get_models.py
```

### エージェントを実行

基本的な実行方法:
```bash
python agent.py "こんにちは"
```

#### オプション引数

- `--model-id`: 使用するモデルIDを指定（デフォルト: `anthropic.claude-3-5-sonnet-20240620-v1:0`）
- `--temperature`: モデルの温度パラメータを指定（デフォルト: `0.3`）
- `--profile`: AWSプロファイル名を指定（デフォルト: `default`）
- `--region`: AWSリージョン名を指定（デフォルト: `us-east-1`）

#### 使用例

```bash
# カスタムプロンプトで実行
python agent.py "今日の天気を教えて"

# モデルと温度を指定して実行
python agent.py "複雑な質問を..." --model-id "anthropic.claude-3-7-sonnet-20250219-v1:0" --temperature 0.7

# カスタムAWSプロファイルとリージョンを指定
python agent.py "こんにちは" --profile my-profile --region ap-northeast-1
```

`agent.py` では、`BedrockModel` を使用して Claude モデルを初期化し、シンプルなエージェントを作成しています。コマンドライン引数を使用して、モデルやAWSの設定を柔軟に変更できます。

## ライセンス

このプロジェクトは [LICENSE](LICENSE) で指定されたライセンスの下で公開されています。
