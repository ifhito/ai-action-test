# Test Documentation Set for Lightweight RAG CI

このディレクトリは、CI内での軽量RAGパイプラインを検証するためのテスト用ドキュメントを格納します。Pull Requestレビュー時に検索したい設計・テスト仕様のサンプルを含んでいます。

- `architecture.md`: RAGベースのCI構成の概要。
- `test-plan.md`: RAGパイプラインを検証するためのテスト計画。
- `embedding-policy.md`: ドキュメントの分割とベクトル化ルール。

各ファイルはSentence-TransformersとFAISSを用いた検索テストで参照されることを想定しています。英語/日本語の両方のクエリで挙動を確認するため、文章はバイリンガルな表現を含めています。
