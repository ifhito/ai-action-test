#!/usr/bin/env python3
"""Query a FAISS index built by build_rag_index.py."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

import faiss  # type: ignore
from sentence_transformers import SentenceTransformer


def load_metadata(metadata_path: Path) -> List[dict]:
    with metadata_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    parser = argparse.ArgumentParser(description="Query docs RAG index")
    parser.add_argument("--index-path", type=Path, default=Path("rag/index.faiss"))
    parser.add_argument("--metadata-path", type=Path, default=Path("rag/docstore.json"))
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    index = faiss.read_index(str(args.index_path))
    metadata = load_metadata(args.metadata_path)

    model = SentenceTransformer(args.model)
    query_embedding = model.encode([args.query], convert_to_numpy=True)

    distances, indices = index.search(query_embedding, args.top_k)

    print(f"Top {args.top_k} results for query: {args.query}")
    for rank, (dist, idx) in enumerate(zip(distances[0], indices[0]), start=1):
        if idx == -1:
            continue
        info = metadata[idx]
        preview = info["text"].splitlines()[0]
        print(f"{rank}. {info['source_path']} (chunk {info['chunk_id']}) - distance={dist:.4f}")
        print(f"   {preview[:160]}{'...' if len(preview) > 160 else ''}")


if __name__ == "__main__":
    main()
