# ai-action-test

テスト用リポジトリとして、CI内で軽量RAGパイプラインを構築・検証するための最小構成を用意しています。

## 構成
- `docs/`: Sentence-TransformersとFAISSでベクトル化するテスト用ドキュメント（CI動作に合わせたアーキテクチャ説明や、共有ToDoアプリの設計例を含む）。
- `scripts/build_rag_index.py`: Markdownをチャンク化し、FAISSインデックスとメタデータを生成するスクリプト。既定では多言語対応の`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`を利用します。
- `scripts/query_rag_index.py`: 生成済みインデックスに対してクエリを投げるためのCLI。同じ多言語モデルを用いて検索クエリを埋め込み化します。
- `.github/workflows/rag-ci.yml`: GitHub Actionsでの検証ワークフロー。依存関係のインストール、インデックス生成、サンプルクエリの実行、アーティファクトのアップロードを行います。
- `requirements.txt`: CIで利用するPython依存。

## ローカルでの試験実行
```bash
python -m venv .venv
source .venv/bin/activate
pip install "numpy<2"
pip install -r requirements.txt
python scripts/build_rag_index.py --docs docs
python scripts/query_rag_index.py --query "CI Flow"
python scripts/query_rag_index.py --query "テスト計画"
```

これにより`rag/index.faiss`と`rag/docstore.json`が生成され、クエリ結果が出力されます。

> **Note:** GitHub Actionsホストでは既定でNumPy 2.xが導入されるため、FAISSホイールと互換性を保つには`numpy<2`を事前にインストールしてから残りの依存関係を入れる必要があります。

## 事前生成済みインデックスの参照

GitHub Actions内でのインデックス再生成が不要な場合は、上記手順でローカル生成した`rag/index.faiss`と`rag/docstore.json`をリポジトリにコミットしておくこともできます。

ワークフローは両ファイルの存在を検出するとビルド処理をスキップし、既存のインデックスをそのままクエリに利用します。大きなモデルを使う負荷が高いケースや、生成結果を固定したい検証時に便利です。
