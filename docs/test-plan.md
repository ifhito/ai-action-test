# Lightweight RAG CI Test Plan

このテスト計画は、GitHub Actions上で軽量RAGパイプラインが期待通りに動作するかを検証するためのものです。

## Test Items
1. **依存関係のインストール**
   - `numpy<2`が先にインストールされ、`requirements.txt`からfaiss-cpuおよびsentence-transformersが正しくインストールできること。
2. **インデックス生成**
   - `scripts/build_rag_index.py`がMarkdownをチャンク化し、FAISSインデックスとメタデータJSONを生成すること。
   - 生成されたメタデータにはファイルパス、チャンクID、テキストが含まれること。
3. **検索CLIの動作確認**
   - 代表的な検索語（例: "CI Flow"、"テスト計画"）に対して、関連するドキュメントを上位に返すこと。
   - 検索結果がCIログに表示され、Pull Requestレビュー時に参照できること。

## Test Data
- `docs/architecture.md`、`docs/embedding-policy.md`などのMarkdownファイルを使用します。

## Exit Criteria
- すべてのテスト項目が成功し、CIジョブが成功で終了すること。
- FAISSインデックスとメタデータファイルが生成されること（事前生成済みファイルがある場合は再生成がスキップされることを確認）。
