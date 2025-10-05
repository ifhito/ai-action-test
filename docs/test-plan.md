# Lightweight RAG CI Test Plan

このテスト計画は、GitHub Actions上で軽量RAGパイプラインが期待通りに動作するかを検証するためのものです。

## Test Items
1. **依存関係のインストール**
   - `numpy<2`が先にインストールされ、`requirements.txt`からfaiss-cpuおよびsentence-transformersが正しくインストールできること。
2. **インデックス生成**
   - `scripts/build_rag_index.py`がMarkdownをチャンク化し、FAISSインデックスとメタデータJSONを生成すること。
   - 生成されたメタデータにはファイルパス、チャンクID、テキストが含まれること。
   - `docs/designs/shared-todo-app/`配下の分割ドキュメントもすべて取り込まれること。
3. **検索CLIの動作確認**
   - 代表的な検索語（例: "CI Flow"、"テスト計画"、"ゲストアクセスの認証"、"Kafka障害"）に対して、関連するドキュメントを上位に返す
     こと。
   - 認証やDDD関連のクエリが、それぞれ`workflows.md`や`domain-driven-design.md`など適切なファイルを参照すること。
   - 検索結果がCIログに表示され、Pull Requestレビュー時に参照できること。

## Test Data
- `docs/architecture.md`、`docs/embedding-policy.md`などのMarkdownファイル。
- `docs/designs/shared-todo-app/`以下のモジュール化された設計資料（ユースケース図、フローチャート、技術仕様、運用手順など）。

## Exit Criteria
- すべてのテスト項目が成功し、CIジョブが成功で終了すること。
- FAISSインデックスとメタデータファイルが生成されること（事前生成済みファイルがある場合は再生成がスキップされることを確認）。
- サンプルクエリの結果が期待する設計資料のパスを含んでいること。
