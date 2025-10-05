# Lightweight RAG CI Architecture

この文書では、Pull Requestレビューを支援するための軽量RAGパイプラインの構成を説明します。

## Goals
- ドキュメントをSentence-Transformersで埋め込み化し、FAISSで高速検索できるようにする。
- CI内で再現可能な形でインデックスを生成し、Pull Requestごとに差分を確認できるようにする。
- 依存関係は最小限にし、GitHub Actions上で動作することを確認する。

## Components
1. **Document Collector**: `docs/`以下のMarkdownファイルを再帰的に取得します。
2. **Chunker**: 500文字を目安に文脈を保ったまま分割し、メタデータとして元のファイルパスを保持します。
3. **Embedder**: 多言語対応の`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`モデルを用いて各チャンクをベクトル化します。日本語クエリでも再現性を持たせるため、このモデルを既定とします。
4. **Vector Store**: FAISSの`IndexFlatL2`を用いてベクトルを格納します。
5. **Query CLI**: Pull Requestレビュー時に「この仕様はどこ？」といった問いを投げられるよう、シンプルな検索CLIを用意します。

## CI Flow
1. Python依存をインストールします（FAISSホイールの互換性を保つため、NumPyは`<2`に固定します）。
2. `scripts/build_rag_index.py`を実行してインデックスを生成します（`rag/index.faiss`と`rag/docstore.json`が既に存在する場合はスキップされます）。
3. `scripts/query_rag_index.py`で代表的な質問を実行し、結果をCIログに表示します。
4. 生成物はアーティファクトとして保存するか、必要に応じてPull Requestコメントへ活用します。

## Future Extensions
- OpenAIなどのLLM APIと組み合わせて、検索結果から回答テンプレートを生成。
- PR差分をもとに更新されたチャンクのみ再計算する差分ベクトル更新。
- docs以外（例: ADR, 設計図）の取り込みや、マルチモーダル化。
