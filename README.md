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

```bash
python agent.py
```

`agent.py` では、`BedrockModel` を使用して Claude モデルを初期化し、シンプルなエージェントを作成しています。

## ライセンス

このプロジェクトは [LICENSE](LICENSE) で指定されたライセンスの下で公開されています。
