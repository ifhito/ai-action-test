# 技術仕様 / Technical Specifications

## アーキテクチャ要約 / Architecture Summary
- **フロントエンド**: React + TypeScript（Web）、React Native（モバイル）。Apollo ClientでGraphQL連携。
- **BFF / API Gateway**: Apollo Federation Gateway。各サービスへのルーティングと認証コンテキスト付与を担当。
- **マイクロサービス**:
  - Task Service（Go + gRPC）
  - Collaboration Service（Node.js + NestJS）
  - Notification Service（Python + FastAPI）
  - Identity Service（Rust + Axum）
  - Analytics Service（Scala + Akka Streams）
- **データストア**: PostgreSQL、Redis、Elasticsearch、Kafka、S3。

## 認証・認可 / Authentication & Authorization
- OIDCプロバイダー（Auth0/Okta）と連携し、PKCE + Authorization Code Flowを採用。
- ゲストアクセスはメールベースOTP + Magic Linkで実装し、`guest_session`スコープを付与。
- 多要素認証: WebAuthn（プライマリ）、TOTPバックアップコード。
- セッション管理:
  - アクセストークン: 15分有効。
  - リフレッシュトークン: 24時間有効でローテーション必須。
  - デバイスバインディング: フィンガープリントハッシュでセッション窃取を検知。
- RBAC: Workspace単位のロール（Owner/Member/Viewer/Guest）。
- ABAC: タスクのラベル（Confidentialなど）に応じた属性ベース制御。
- SCIM APIでエンタープライズユーザーのプロビジョニングを自動化。

## API仕様 / API Specifications
- GraphQL Schemas:
  - `type Task { id: ID!, title: String!, description: String, status: TaskStatus!, checklist: [ChecklistItem!]! }`
  - Mutations: `createTask`, `assignTask`, `updateTaskStatus`, `scheduleReminder`, `shareTaskWithGuest`。
  - Subscriptions: `taskUpdated`, `commentAdded`, `reminderTriggered`。
- REST Endpoints:
  - `POST /auth/guest/otp`（OTP生成）
  - `POST /auth/guest/verify`（OTP検証）
  - `POST /webhooks/calendar/export`
  - `GET /audit/events?actorId=&from=&to=`
- gRPC Services:
  - `NotificationService.SendBatch(NotificationBatch)`
  - `AnalyticsService.StreamEvents(EventRequest)`

## イベント駆動連携 / Event-Driven Integration
- Kafka Topics:
  - `task-events`: Task Serviceが発行するステータス変更、コメント作成、依存関係更新。
  - `notification-delivery`: Notification Serviceが発行する配送結果。
  - `audit-events`: Identity/Task/Collaborationが共通スキーマで発行。
- 逆方向同期: Analyticsが異常検知イベントを`incident-alerts`トピックで通知し、Notificationがインシデントチャンネルへ送信。

## 非機能要件 / Non-Functional Requirements
- SLA: 99.9% uptime、月間ダウンタイム < 43分。
- パフォーマンス: タスク一覧APIのp95 < 250ms（キャッシュヒット時は80ms以下）。
- 可用性: 各サービスは2リージョンでアクティブ-アクティブ構成。リーダー選出はConsul。
- セキュリティ: 全APIはTLS1.2以上を強制。CSPヘッダーを厳格化し、`strict-dynamic`を採用。
- プライバシー: PIIはField-level encryptionで保存。Data Residencyに応じたKMSキーを利用。

## 監視とアラート / Observability & Alerting
- 指標: Prometheusメトリクス（レイテンシ、エラーレート、通知配送成功率）。
- ロギング: OpenTelemetry TraceをZipkin互換エンドポイントにエクスポート。監査ログはセキュアストレージへ。
- アラートポリシー: 3分間のp95レイテンシが閾値超過でPagerDutyに通知。セキュリティイベントはSplunk PhantomでSOAR連携。
- ダッシュボード: Grafanaでサービス単位・ロール単位の使用状況を可視化。

## テスト戦略 / Testing Strategy
- コンシューマ契約テスト: GraphQL Federation用にApollo Studioの契約チェックをCIで実行。
- セキュリティテスト: OpenIDフローのペネトレーションテスト、OWASP ASVS Level 2準拠のチェックリスト。
- パフォーマンステスト: k6でWeb/APIロードテスト、LocustでモバイルAPIのスパイクテスト。
- レジリエンス: Chaos Engineering（Gremlin）で通知サービスの遅延/失敗をシミュレーション。

## リリースポリシー / Release Policy
- 週次の安定リリースとオンデマンドのホットフィックス。
- Feature FlagをLaunchDarklyで管理し、段階的ロールアウト。
- ブルー/グリーンデプロイを採用し、リグレッション検知時は即時ロールバック。

## セキュリティ考慮事項 / Security Considerations
- 秘密情報はHashiCorp Vaultで管理し、CI/CDには短期トークンを発行。
- ゲスト共有リンクは1時間で失効し、範囲外アクセスは自動で遮断。
- DLP: 添付ファイルはマルウェアスキャン後に暗号化してS3へ保存。PII検知時は自動マスク。
- ゼロトラスト: すべての内部APIコールに対してmTLSを強制し、SPIFFE/SPIREでアイデンティティを配布。
