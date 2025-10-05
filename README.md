# ai-action-test

テスト用リポジトリとして、CI内で軽量RAGパイプラインを構築・検証するための最小構成を用意しています。

## 構成
- `docs/`: Sentence-TransformersとFAISSでベクトル化するテスト用ドキュメント。CI動作に合わせたアーキテクチャ説明や、共有ToDoアプリ
  のモジュール化された設計例を含みます。
  - `docs/designs/shared-todo-app.md`および配下のファイルでは、フローチャート、シーケンス図、DDD、認証仕様、運用ガイドを個別のMarkdown
    に分割しており、多視点クエリを想定したRAGテストデータを提供します。
- `scripts/build_rag_index.py`: Markdownをチャンク化し、FAISSインデックスとメタデータを生成するスクリプト。既定では多言語対応の
  `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`を利用します。
- `scripts/query_rag_index.py`: 生成済みインデックスに対してクエリを投げるためのCLI。同じ多言語モデルを用いて検索クエリを埋め込み化
  します。
- `.github/workflows/rag-ci.yml`: GitHub Actionsでの検証ワークフロー。依存関係のインストール、インデックス生成、サンプルクエリの実行、
  アーティファクトのアップロードを行います。
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
python scripts/query_rag_index.py --query "ゲストアクセスの認証"
```

これにより`rag/index.faiss`と`rag/docstore.json`が生成され、クエリ結果が出力されます。

> **Note:** GitHub Actionsホストでは既定でNumPy 2.xが導入されるため、FAISSホイールと互換性を保つには`numpy<2`を事前にインストールして
> から残りの依存関係を入れる必要があります。

## 事前生成済みインデックスの参照

GitHub Actions内でのインデックス再生成が不要な場合は、上記手順でローカル生成した`rag/index.faiss`と`rag/docstore.json`をリポジトリにコ
ミットしておくこともできます。

ワークフローは両ファイルの存在を検出するとビルド処理をスキップし、既存のインデックスをそのままクエリに利用します。大きなモデルを使
う負荷が高いケースや、生成結果を固定したい検証時に便利です。
