# ユースケースとシナリオ / Use Cases & Scenarios

```mermaid
usecaseDiagram
  title Shared ToDo Collaboration Use Cases
  actor PM as "Project Manager"
  actor Member as "Team Member"
  actor Guest as "Guest Collaborator"
  actor Auditor as "Security Auditor"

  PM --> (Plan Sprint)
  PM --> (Invite Members)
  PM --> (Configure Notifications)

  Member --> (Update Task Status)
  Member --> (Comment on Task)
  Member --> (Sync Calendar)

  Guest --> (View Shared Task)
  Guest --> (Leave Guest Comment)

  Auditor --> (Review Audit Logs)
  Auditor --> (Export Compliance Report)

  (Plan Sprint) ..> (Prioritize Backlog) : include
  (Plan Sprint) ..> (Assign Tasks) : include
  (Configure Notifications) ..> (Set Reminder Policy) : extend
  (Update Task Status) ..> (Trigger Notifications) : extend
```

## 主要シナリオ / Primary Scenarios

1. **スプリント計画 / Sprint Planning**
   - PMがバックログからタスクを選び、ストーリーポイントを付与。
   - 優先順位が決まるとGraphQL Mutation `assignTasks`が呼ばれ、Notification Serviceへイベントが発火。
   - メンバーにはSlack Webhookとアプリ内通知が同時に送信される。

2. **モバイルからのステータス更新 / Mobile Status Update**
   - DeveloperがReact Nativeアプリでタスクを「In Progress」へ変更。
   - オフラインだった場合はローカルキューに保持し、オンライン復帰時に差分同期APIへ送信。
   - Task Serviceが状態遷移を検証し、Auditイベントを記録してから通知をブロードキャスト。

3. **ゲストコメント / Guest Commenting**
   - PMが特定タスクの限定共有リンクを生成。ゲストはメールOTPによるワンタイムログイン。
   - 権限はコメント作成と添付ファイルアップロードに限定され、閲覧ログが10分間隔で監査ストレージに保存される。

4. **監査レポート / Audit Reporting**
   - Security Auditorが月次のアクセスレポートを要求。
   - `audit-report-generator` LambdaがEventBridgeスケジュールで起動し、CloudTrailとイベントストアから集計。
   - 結果はS3に暗号化して保存し、監査ダッシュボードにリンクされる。

## 代替フロー / Alternate Flows
- **タスク重複検知**: 同一タイトルと期限のタスクが作成されると、Task Serviceが`409 Conflict`を返し、類似候補をレスポンスで提示。
- **コメントモデレーション**: 不適切なワードが含まれた場合は機械学習フィルターが警告を返し、モデレータの承認が必要。
- **通知スロットリング**: 1分以内に同一タスクで10件以上のイベントが発生すると、通知サービスがバッチングしてDigestメールを送信。

## QA観点のトレーサビリティ / QA Traceability
- ユースケースIDをテストケースに紐づけ、CI内での自動チェック結果とリンクさせることで、どのシナリオが満たされているかを可視化できま
す。
