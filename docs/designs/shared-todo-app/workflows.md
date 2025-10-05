# 業務フロー / Workflows

## タスク作成と共有フロー / Task Creation & Sharing
```mermaid
flowchart TD
  A[Task idea captured] --> B{Workspace selected?}
  B -- yes --> C[Create task draft]
  B -- no --> D[Create new workspace]
  D --> C
  C --> E[Assign members]
  E --> F{Need guest access?}
  F -- yes --> G[Generate guest invitation]
  F -- no --> H[Skip guest invitation]
  G --> I[Send OTP email]
  H --> J[Persist task]
  I --> J
  J --> K[Emit domain event]
  K --> L[Trigger notifications]
  K --> M[Update analytics]
```

## 認証とセッション管理フロー / Authentication & Session Management
```mermaid
flowchart LR
  Start((Start)) --> Detect[Detect login entrypoint]
  Detect -->|SSO| OIDC[Redirect to OIDC Provider]
  Detect -->|Email OTP| OTP[Send One-Time Password]
  OIDC --> Callback[Handle OIDC callback]
  OTP --> VerifyOTP[Verify OTP code]
  Callback --> TokenIssue[Issue access & refresh tokens]
  VerifyOTP --> TokenIssue
  TokenIssue --> MFA{MFA required?}
  MFA -- yes --> Challenge[Prompt WebAuthn challenge]
  Challenge --> TokenUpdate[Bind MFA claim]
  MFA -- no --> TokenUpdate
  TokenUpdate --> SessionStore[Persist session + device fingerprint]
  SessionStore --> PolicyEval[Evaluate RBAC & ABAC policies]
  PolicyEval --> IssueCookie[Set secure cookies / headers]
  IssueCookie --> End((Authenticated))
```

## コメントモデレーションフロー / Comment Moderation
```mermaid
flowchart TD
  Draft[Comment submitted] --> Precheck[Run profanity filter]
  Precheck -->|Clean| Publish[Store comment]
  Precheck -->|Flagged| ReviewQueue[Add to moderation queue]
  ReviewQueue --> Decision{Approve or Reject}
  Decision -->|Approve| Publish
  Decision -->|Reject| NotifyAuthor[Notify author with reason]
  Publish --> NotifySubscribers[Notify subscribers]
  NotifySubscribers --> Analytics[Log engagement metrics]
  NotifyAuthor --> Analytics
```

## SLA違反検知フロー / SLA Breach Detection
```mermaid
flowchart LR
  Metrics[Collect p95 latency metrics] --> Window[Sliding window aggregation]
  Window --> Threshold{p95 > 300ms?}
  Threshold -- no --> Healthy[Mark service healthy]
  Threshold -- yes --> Incident[Open incident in PagerDuty]
  Incident --> AutoScale[Trigger auto-scaling rule]
  AutoScale --> Reeval[Re-evaluate metrics]
  Reeval --> Threshold
  Incident --> Postmortem[Create post-incident task]
```

各フローチャートはCI内のRAG検索テストで、特定のフローに関する質問（例: 「OTPログインの流れは？」）へ素早くリンクできるよう設計されています。
