# デプロイと運用 / Deployment & Operations

## 環境構成 / Environments
- **Sandbox**: 個人検証用。Feature Flagを自由に切り替え可能。自動削除: 7日。
- **Staging**: 本番同等構成。夜間に自動データリフレッシュ。SSOはテストIdPを使用。
- **Production**: マルチリージョン（ap-northeast-1, us-east-1）。Route53でWeighted Routing。

## インフラストラクチャ / Infrastructure
- Kubernetes (EKS) 上で各マイクロサービスをデプロイ。Istioでサービスメッシュ化。
- データベースはAmazon RDS for PostgreSQL（マルチAZ）。RedisはAmazon ElastiCache。
- オブジェクトストレージはAmazon S3。監査ログはS3 Glacier Deep Archiveへライフサイクル移行。
- KafkaクラスターはMSK（3ノード）、Schema RegistryはConfluent互換。

## CI/CD パイプライン / CI/CD Pipeline
- GitHub Actionsでビルド→テスト→セキュリティスキャン（Snyk）→イメージ署名（cosign）。
- Argo CDが署名済みマニフェストを取得し、各環境へGitOpsデプロイ。
- カナリアリリース: `prod-canary` namespaceで10%トラフィックを新バージョンへ。メトリクスが安定後100%へ昇格。
- ロールバックはArgo CDのアプリケーション履歴から1クリックで実施可能。

## 運用手順 / Operational Runbooks
- **インシデント対応**: PagerDutyでオンコールに通知 → Slackの`#incident`チャンネルでブリッジ → Zoom自動立ち上げ。
- **キー管理**: KMSキーのローテーションは90日ごと。Vaultのルートトークンは封印保管。
- **アクセスレビュー**: 月次でWorkspace権限の棚卸しを自動レポート化。承認フローはServiceNow。

## 障害シナリオ / Failure Scenarios
- **Kafka障害**: Circuit Breakerが動作し、イベント書き込み失敗時はS3バックアップキューへフォールバック。復旧後リプレイ。
- **リージョン停止**: Route53ヘルスチェックで異常検知 → トラフィックを代替リージョンへ100%切替 → Aurora Global Databaseでフェイルオーバー。
- **Auth0障害**: キャッシュされたサービスアカウントとEmergency Adminを用いて限定的な管理アクセスを維持。

## コンプライアンス / Compliance
- SOC2 Type II、ISO27001に準拠した統制。
- 監査証跡はImmutable Storageへ書き込み、アクセスはRBAC + Just-In-Time承認。
- データ保護影響評価（DPIA）を年次実施。

## 運用メトリクス / Operational Metrics
| 指標 | 目標 | 備考 |
| --- | --- | --- |
| MTTR | < 30分 | インシデントレビューで継続改善。 |
| Error Budget Burn | < 25%/四半期 | SLO 99.9%基準。 |
| 変更失敗率 | < 5% | ロールバック件数/総デプロイ数。 |
| アラートノイズ | < 3件/週 | ノンアクションアラートを削減。 |

## RAG観点での利用 / Usage in RAG Workflows
- CIで`deployment-and-ops.md`を参照し、障害シナリオに関する質問（例: 「Kafka障害時のフォールバックは？」）の回答源として利用。
- FlowやRunbookを分割管理することで、Pull Requestレビューでの差分確認が容易になります。
