# Embedding Policy for CI RAG Tests

この文書は、テスト用軽量RAGパイプラインにおけるドキュメント分割と埋め込みのルールを示します。

## Chunking Rules
- Markdownの見出しごとに段落をグルーピングし、最大500文字になるよう調整します。
- 500文字を超える場合は文末で区切り、文脈を保つために重なりを50文字確保します。
- チャンクには`source_path`、`chunk_id`、`text`のメタデータを付与します。
- Mermaidコードブロック（フローチャート、シーケンス図、ユースケース図）は、それぞれ単一チャンクとして保持し、図に関連する説明文と
  ペアで保存します。

## Embedding Rules
- モデル: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`（日本語/英語のクエリ双方を想定）。
- ベクトル化はバッチサイズ32を目安とし、CI時間短縮のためGPUは想定しません。
- 生成したベクトルはFAISSのL2距離で比較します。
- 認証・運用のような専門用語を含むチャンクは、そのままの用語（例: WebAuthn, SCIM, Zero Trust）を保持して翻訳ロスを回避します。

## Validation
- 代表的な検索クエリ: "CI Flow"、"差分ベクトル更新"、"アーティファクト"、"テスト計画"、"ゲストアクセスの認証"、"Kafka障害"。
- クエリ結果には関連ドキュメントのタイトルと元ファイルパスを表示します。
- 新たに追加した設計資料（例: `designs/shared-todo-app/technical-specs.md`）が検索上位に現れることをレビューで確認します。
