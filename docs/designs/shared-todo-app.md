# 共有可能なToDoアプリ設計書（分割版） / Shared ToDo App Design (Modular)

この設計書は複数の観点に分割され、詳細なドキュメントは`shared-todo-app/`ディレクトリ以下に格納されています。Pull RequestレビューやRAG
検索で、必要な観点のみ迅速に参照できる構成です。

## クイックリンク / Quick Links
- [プロダクトビジョンとペルソナ](shared-todo-app/vision-and-personas.md)
- [ユースケースとシナリオ](shared-todo-app/use-cases.md)
- [ドメイン駆動設計](shared-todo-app/domain-driven-design.md)
- [データモデルとイベントスキーマ](shared-todo-app/data-model.md)
- [業務フロー（フローチャート）](shared-todo-app/workflows.md)
- [シーケンス図](shared-todo-app/sequence-diagrams.md)
- [技術仕様（認証・API・非機能）](shared-todo-app/technical-specs.md)
- [デプロイと運用](shared-todo-app/deployment-and-ops.md)

## 目的 / Purpose
- 設計変更時に、どのコンポーネントやフローが影響を受けるかを素早く把握する。
- CIの軽量RAG検索で、特定の質問（例: 「ゲストアクセスの認証方法は？」）に対応するドキュメントを即座に引き当てる。
- 認証、通知、監査などの非機能要件も含めた包括的な設計資料を提供する。

## 変更履歴 / Changelog Snapshot
- 2024-05: 認証ハンドシェイク、コメントモデレーションなどのフローをMermaid図で追加。
- 2024-05: DDD観点の境界づけられたコンテキストとユビキタス言語を整理。
- 2024-05: 技術仕様にゼロトラスト認証、SCIM、監査レポート生成手順を追加。

詳細は各ドキュメントを参照してください。
