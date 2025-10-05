# Embedding Policy for CI RAG Tests

この文書は、テスト用軽量RAGパイプラインにおけるドキュメント分割と埋め込みのルールを示します。

## Chunking Rules
- Markdownの見出しごとに段落をグルーピングし、最大500文字になるよう調整します。
- 500文字を超える場合は文末で区切り、文脈を保つために重なりを50文字確保します。
- チャンクには`source_path`、`chunk_id`、`text`のメタデータを付与します。

## Embedding Rules
- モデル: `sentence-transformers/all-MiniLM-L6-v2`
- ベクトル化はバッチサイズ32を目安とし、CI時間短縮のためGPUは想定しません。
- 生成したベクトルはFAISSのL2距離で比較します。

## Validation
- 代表的な検索クエリ: "CI Flow"、"差分ベクトル更新"、"アーティファクト"。
- クエリ結果には関連ドキュメントのタイトルと元ファイルパスを表示します。
