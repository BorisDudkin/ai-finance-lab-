"""
LLM-based macro regime classifier for asset allocation.

This module provides `classify_macro(text)` which calls the repository's
`llm_client.call_llm(messages, temperature=...)` interface and returns the raw
LLM response string.
"""

from typing import List, Dict
import argparse

from llm_client import call_llm
from pathlib import Path


def classify_macro(text: str) -> str:
    """Classify macro/regime text using the configured LLM.

    Uses a conservative system message and `temperature=0.0` for deterministic outputs.
    """
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": "Be conservative and precise."},
        {"role": "user", "content": text},
    ]
    try:
        return call_llm(messages, temperature=0.0)
    except Exception as exc:
        # Raise a clearer, testable error for callers
        raise RuntimeError("LLM call failed in classify_macro") from exc


def main() -> None:
    """CLI entrypoint: read text from a file and print classification.

    Default file is `sample_inputs/fomc.txt` located relative to this module.
    """
    parser = argparse.ArgumentParser(description="Classify macro text using LLM.")
    default_sample = Path(__file__).resolve().parent.joinpath("sample_inputs", "fomc.txt")
    parser.add_argument(
        "--file",
        "-f",
        default=str(default_sample),
        help=f"Path to text file to classify (default: {default_sample})",
    )
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        raise SystemExit(f"Error: file not found: {file_path}")

    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception as exc:
        raise SystemExit(f"Error reading file {file_path}: {exc}")

    print(classify_macro(text))


if __name__ == "__main__":
    main()
