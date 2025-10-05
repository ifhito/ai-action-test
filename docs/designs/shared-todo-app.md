# 共有可能なToDoアプリ設計書

この文書では、チームメンバーとタスクを共有しながら管理できるToDoアプリの例示的な設計を示します。軽量RAGのサンプルコンテンツとして利用できるように、要件、アーキテクチャ、データモデル、API、運用フローを整理しています。

## ビジョンとユースケース
- 個人とチームの両方で利用でき、タスクの状態・担当者・期限を共有できる。
- モバイルとWebの両方からアクセスできるレスポンシブUI。
- コメントやメンションでコミュニケーションを補助する。
- 外部サービス（Googleカレンダー等）との連携を想定したWebhook/ICSエクスポート。

## ユーザーロール
| ロール | 説明 | 主な権限 |
| --- | --- | --- |
| Owner | ワークスペースの作成者。課金管理とメンバー管理が可能。 | 招待、権限変更、課金設定 |
| Member | タスクを作成・編集できる一般ユーザー。 | タスクCRUD、コメント、リマインダー設定 |
| Viewer | 参照専用ユーザー。閲覧のみ可能。 | タスク閲覧、コメント閲覧 |

## 全体アーキテクチャ
```
React(Web) / React Native(App)
           |
    GraphQL API Gateway
           |
   ---------------------------------
   |              |                |
 Task Service  Comment Service  Notification Service
   |              |                |
 PostgreSQL   PostgreSQL        Redis + SES/FCM
```
- **GraphQL API Gateway**: BFFとして認証済みユーザーコンテキストを付与し、各サービスの集約ポイントとなる。
- **Task Service**: タスク、リスト、ステータス管理を担当。タスクとユーザーの多対多関係を扱う。
- **Comment Service**: コメントやメンション、変更履歴を保持。イベントソーシングで変更ログを記録。
- **Notification Service**: リマインダーや共有更新通知をRedisベースのジョブキューで処理。

## データモデル
- `users` (id, name, email, locale, timezone)
- `workspaces` (id, name, billing_plan)
- `workspace_members` (workspace_id, user_id, role)
- `task_lists` (id, workspace_id, name, color)
- `tasks` (id, task_list_id, title, description, due_at, status, priority)
- `task_assignees` (task_id, user_id)
- `comments` (id, task_id, author_id, body, mentions, created_at)
- `notifications` (id, user_id, channel, payload, deliver_at, delivered_at)

## API設計（抜粋）
### GraphQL Mutation: `createTask`
- 入力: `title`, `description`, `dueDate`, `assigneeIds`, `listId`
- ビジネスルール:
  - 期限はユーザーのタイムゾーンで正規化。
  - アサイン対象は同一ワークスペースメンバーに限定。
  - 作成時にデフォルトリマインダー（期限24時間前）をNotification Serviceへ登録。

### GraphQL Subscription: `taskUpdated`
- クライアントは`taskId`または`listId`を指定してサブスクライブ。
- 変更が発生した際、Diffを含むペイロードをPush。
- コメント追加やステータス変更にも対応。

### REST Endpoint: `POST /integrations/calendar/export`
- ワークスペース単位で公開鍵を生成し、ICSファイルを生成。
- タスクの期限変更が発生するとNotification Serviceが差分生成をトリガー。

## 共有と同期戦略
- WebSocketを利用した双方向同期。GraphQL SubscriptionsはApollo Federationを利用。
- オフライン対応: モバイルアプリはIndexedDB/SQLiteへローカルキャッシュ。再接続時に差分同期APIを叩く。
- 変更競合は楽観的ロック（`updated_at`チェック）で解決し、失敗時は最新状態をクライアントへ返す。

## セキュリティと権限
- CognitoやAuth0などのOIDCプロバイダーと連携し、JWTをGraphQL Gatewayで検証。
- ワークスペースごとにRBACポリシーを付与。GraphQLリゾルバーで権限評価。
- 監査ログはComment ServiceのイベントストアとCloudWatch Logsへ二重書き込み。

## 非機能要件
- SLA: 99.9%稼働。タスク作成APIのp95レイテンシ < 300ms。
- スケーラビリティ: Notification Serviceは水平スケール可能なワーカーを提供。
- コンプライアンス: 主要リージョン（東京、シンガポール、バージニア）でデータレジデンシを選択可能。

## テスト計画の観点
- GraphQLスキーマの自動生成テスト。
- 各サービスのContract Test（Task⇔Notification）。
- E2E: CypressでWeb UI、Detoxでモバイルをカバー。

## 今後の拡張
- タスクテンプレートの共有や自動生成。
- AIによるタスク分類と優先度推定。
- ドキュメント紐付け（Notion/Confluence連携）。
