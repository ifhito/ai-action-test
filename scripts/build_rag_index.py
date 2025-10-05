#!/usr/bin/env python3
"""Build a FAISS index from Markdown documents for CI RAG tests."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List

import faiss  # type: ignore
from sentence_transformers import SentenceTransformer


@dataclass
class Chunk:
    source_path: str
    chunk_id: int
    text: str

    def to_record(self) -> dict:
        record = asdict(self)
        record["token_length"] = len(self.text.split())
        return record


def iter_markdown_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*.md")):
        if path.is_file():
            yield path


def chunk_text(text: str, max_chars: int = 500, overlap: int = 50) -> List[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: List[str] = []
    buffer = ""

    def flush_buffer(current: str) -> None:
        if current:
            chunks.append(current.strip())

    for para in paragraphs:
        candidate = (buffer + "\n\n" + para).strip() if buffer else para
        if len(candidate) <= max_chars:
            buffer = candidate
            continue
        if buffer:
            flush_buffer(buffer)
            buffer = ""
        while len(para) > max_chars:
            split_point = para.rfind("。", 0, max_chars)
            if split_point == -1:
                split_point = max_chars
            chunk = para[:split_point].strip()
            flush_buffer(chunk)
            para = para[max(0, split_point - overlap) :].strip()
        buffer = para
    flush_buffer(buffer)
    return chunks


def build_chunks(docs_root: Path) -> List[Chunk]:
    chunks: List[Chunk] = []
    for md_path in iter_markdown_files(docs_root):
        relative = md_path.relative_to(docs_root.parent if docs_root.is_absolute() else Path("."))
        text = md_path.read_text(encoding="utf-8")
        for idx, chunk in enumerate(chunk_text(text)):
            chunks.append(Chunk(source_path=str(relative), chunk_id=idx, text=chunk))
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Build FAISS index for docs")
    parser.add_argument("--docs", type=Path, default=Path("docs"), help="Root directory containing markdown files")
    parser.add_argument("--index-path", type=Path, default=Path("rag/index.faiss"), help="Path to save FAISS index")
    parser.add_argument(
        "--metadata-path", type=Path, default=Path("rag/docstore.json"), help="Path to save chunk metadata"
    )
    parser.add_argument(
        "--model",
        default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        help="Sentence-Transformers model name",
    )
    parser.add_argument("--batch-size", type=int, default=32, help="Embedding batch size")
    args = parser.parse_args()

    docs_root = args.docs
    if not docs_root.exists():
        raise SystemExit(f"Docs directory not found: {docs_root}")

    chunks = build_chunks(docs_root)
    if not chunks:
        raise SystemExit("No markdown files found to index.")

    model = SentenceTransformer(args.model)
    embeddings = model.encode([chunk.text for chunk in chunks], batch_size=args.batch_size, convert_to_numpy=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    args.index_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(args.index_path))

    args.metadata_path.parent.mkdir(parents=True, exist_ok=True)
    with args.metadata_path.open("w", encoding="utf-8") as f:
        json.dump([chunk.to_record() for chunk in chunks], f, ensure_ascii=False, indent=2)

    print(f"Indexed {len(chunks)} chunks from {docs_root} using model {args.model}.")
    print(f"Index saved to {args.index_path}")
    print(f"Metadata saved to {args.metadata_path}")


if __name__ == "__main__":
    main()
