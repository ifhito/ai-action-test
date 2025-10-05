# 共有ToDoコラボレーションアプリ設計インデックス / Shared ToDo Collaboration App Design Index

このディレクトリは、チームで共有できるToDoアプリケーションのリッチな設計資料を複数ファイルに分割して格納しています。Pull Requestレビ
ュー時のRAG検索が、異なる観点（フロー図、ユースケース、DDD、技術仕様など）にまたがるドキュメントを横断できるようにすることが目的で
す。

## ドキュメントマップ / Document Map

| ファイル | 内容 | 用途 |
| --- | --- | --- |
| `vision-and-personas.md` | プロダクトビジョン、ペルソナ、利用シナリオの整理。 | プロダクト戦略の背景理解。 |
| `use-cases.md` | ユースケース図とシナリオ詳細、エッジケース。 | 要求仕様レビュー、QA観点の洗い出し。 |
| `domain-driven-design.md` | 境界づけられたコンテキスト、アグリゲート、ユビキタス言語。 | DDDベースの設計議論、チーム間契約。 |
| `data-model.md` | エンティティと関係、イベントスキーマ。 | DB設計、イベント駆動連携の確認。 |
| `workflows.md` | 複数の業務フローと分岐のフローチャート。 | UX・業務プロセスのレビュー。 |
| `sequence-diagrams.md` | 認証・タスク共有・通知のシーケンス図。 | 通信経路、API呼び出し順の確認。 |
| `technical-specs.md` | 認証、API、非機能要件、監視、セキュリティ。 | 実装計画、SLO・SLA検討。 |
| `deployment-and-ops.md` | 環境構成、運用フロー、リリース戦略。 | SRE/DevOps観点、CI/CD検討。 |

## 利用方法 / How to Use

- 設計レビューでは`vision-and-personas.md`でコンテキストを掴み、`use-cases.md`や`workflows.md`で具体的な体験を確認します。
- 技術的な深掘りでは`domain-driven-design.md`と`technical-specs.md`を参照し、API・イベント契約をレビューします。
- 運用やリリースの検討時には`deployment-and-ops.md`を参照し、監視項目や障害対応手順を確認します。

各ファイルは日本語と英語を交えながら記述されており、Sentence-Transformersによる多言語検索のテストデータとして活用できます。
