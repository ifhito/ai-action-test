# Lightweight RAG CI Architecture

この文書では、Pull Requestレビューを支援するための軽量RAGパイプラインの構成を説明します。

## Goals
- ドキュメントをSentence-Transformersで埋め込み化し、FAISSで高速検索できるようにする。
- CI内で再現可能な形でインデックスを生成し、Pull Requestごとに差分を確認できるようにする。
- 依存関係は最小限にし、GitHub Actions上で動作することを確認する。
- 設計資料をモジュール化し、日本語・英語混在の検索クエリでも関連情報を引き当てられること。

## Components
1. **Document Collector**: `docs/`以下のMarkdownファイルを再帰的に取得します。サブディレクトリ（例: `designs/shared-todo-app/`）
   の個別設計書も対象です。
2. **Chunker**: 500文字を目安に文脈を保ったまま分割し、メタデータとして元のファイルパスを保持します。ユースケース図やシーケンス図とい
   ったMermaidブロックも一緒にチャンク化されます。
3. **Embedder**: 多言語対応の`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`モデルを用いて各チャンクをベクトル化し
   ます。日本語クエリでも再現性を持たせるため、このモデルを既定とします。
4. **Vector Store**: FAISSの`IndexFlatL2`を用いてベクトルを格納します。
5. **Query CLI**: Pull Requestレビュー時に「この仕様はどこ？」といった問いを投げられるよう、シンプルな検索CLIを用意します。

## CI Flow
1. Python依存をインストールします（FAISSホイールの互換性を保つため、NumPyは`<2`に固定します）。
2. `scripts/build_rag_index.py`を実行してインデックスを生成します（`rag/index.faiss`と`rag/docstore.json`が既に存在する場合はスキ
   ップされます）。
3. `scripts/query_rag_index.py`で代表的な質問を実行し、結果をCIログに表示します。英語・日本語のクエリを織り交ぜ、分割された設計書へ
   のリンク性を検証します。
4. 生成物はアーティファクトとして保存するか、必要に応じてPull Requestコメントへ活用します。

## Documentation Topology
- `docs/designs/shared-todo-app.md`は、共有ToDoアプリの設計書インデックスです。配下の`shared-todo-app/`ディレクトリには、
  - フローチャート（`workflows.md`）
  - シーケンス図（`sequence-diagrams.md`）
  - ドメイン駆動設計（`domain-driven-design.md`）
  - 技術仕様と認証設計（`technical-specs.md`）
  といった観点別ファイルが配置されており、RAG検索で差分を把握しやすい粒度に分割されています。
- 認証フローやゲストアクセスの説明は`workflows.md`および`technical-specs.md`で詳細化されています。レビュー時に「OTPの流れ」「ゼロ
  トラスト要件」などの質問を投げると、該当チャンクが返りやすくなります。

## Future Extensions
- OpenAIなどのLLM APIと組み合わせて、検索結果から回答テンプレートを生成。
- PR差分をもとに更新されたチャンクのみ再計算する差分ベクトル更新。
- docs以外（例: ADR, 設計図）の取り込みや、マルチモーダル化。

## 参考アーキテクチャ例
- 共有可能なToDoアプリの設計書は`docs/designs/shared-todo-app/`以下に分割配置されています。
- 実際のマイクロサービス分割、GraphQLゲートウェイ、認証基盤、通知基盤など複数の観点が含まれており、RAG検索のテストデータとして差
  分が出やすい構成になっています。
