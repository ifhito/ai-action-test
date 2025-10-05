# Test Documentation Set for Lightweight RAG CI

このディレクトリは、CI内での軽量RAGパイプラインを検証するためのテスト用ドキュメントを格納します。Pull Requestレビュー時に検索したい
設計・テスト仕様のサンプルを含んでいます。

- `architecture.md`: RAGベースのCI構成の概要。
- `test-plan.md`: RAGパイプラインを検証するためのテスト計画。
- `embedding-policy.md`: ドキュメントの分割とベクトル化ルール。
- `designs/shared-todo-app.md`: チームで共有可能なToDoアプリの設計書インデックス。
  - `designs/shared-todo-app/vision-and-personas.md`: プロダクトビジョンとペルソナ。
  - `designs/shared-todo-app/use-cases.md`: ユースケース図とシナリオ詳細。
  - `designs/shared-todo-app/domain-driven-design.md`: DDD観点の整理。
  - `designs/shared-todo-app/data-model.md`: データモデルとイベントスキーマ。
  - `designs/shared-todo-app/workflows.md`: フローチャート化された業務フロー（認証含む）。
  - `designs/shared-todo-app/sequence-diagrams.md`: 認証・共同編集などのシーケンス図。
  - `designs/shared-todo-app/technical-specs.md`: 認証/認可、API、非機能仕様。
  - `designs/shared-todo-app/deployment-and-ops.md`: デプロイ戦略と運用手順。

各ファイルはSentence-TransformersとFAISSを用いた検索テストで参照されることを想定しています。英語/日本語の両方のクエリで挙動を確認す
るため、文章はバイリンガルな表現を含めています。
