# Copilot / AI agent instructions for ai-finance-lab

Purpose: Give succinct, project-specific guidance so an AI coding agent can be productive immediately.

## Quick start ✅
- Run small scripts directly: `python 01_macro_regime_classifier/classify.py` (uses `sample_inputs/fomc.txt`).
- Typical pattern: import functions and call them from tests or higher-level scripts (no full app server here).

## Key files & folders (what matters) 🔧
- `01_macro_regime_classifier/classify.py` — LLM-based classification. Uses `call_llm(messages, temperature=0.0)`.
- `02_asset_allocation_signals/signals.py` — Generates allocation JSON. Note system prompt: **"Return valid JSON only."** and `json.loads(call_llm(...))`.
- `02_asset_allocation_signals/schema.json` — intended schema for signals (currently empty; update when changing signal shape).
- `03_generative_ai/` — evaluation, RAG artifacts and structured outputs (mostly scaffolding).
- `04_macro_research_rag/query/answer.py` — RAG answering pattern: `answer(question, context_chunks)` concatenates context and asks LLM: **"Answer only from context."**
- `docs/risk_controls.md` and `docs/model_limitations.md` — project guardrails (human-in-the-loop, confidence thresholds, provenance, conservative outputs).
- `05_multi_agent_systems/` and `06_agents/` — higher-level agent/assistant scaffolds used for multi-agent experimentation.

## Project-specific LLM conventions (follow these precisely) 📜
- call signature: `call_llm(messages, temperature=...)` — the repository expects a small wrapper (`llm_client`) that returns raw text. Keep this interface.
- Deterministic outputs: use `temperature=0.0` for tasks that must be machine-parseable (classification, JSON signals).
- Use `system` messages to constrain behavior (examples: "Be conservative and precise.", "Return valid JSON only.", "Answer only from context.").
- When the task expects machine-readable output, embed a clear JSON schema in the user message and parse with `json.loads()`; always wrap parsing with try/except and raise a clear, testable error if parsing fails.
- Include an explicit `confidence` field for graded outputs (0-1) — `signals.py` expects this.

## RAG and provenance patterns 🔍
- RAG query code concatenates text chunks and sends them in a prompt constrained by a system message. Agents should avoid hallucinations by respecting the system message that restricts answers to provided context.
- Preserve source attribution when adding RAG functionality (store chunk ids / filenames alongside chunk text if you add ingestion code).

## Implementation notes & best practices specific to this codebase 💡
- `llm_client` is intentionally external to the repo — when adding it, implement these behaviors:
  - Accept `messages` and `temperature` parameters and return the LLM text response.
  - Read credentials via environment variables (do **not** commit secrets).
  - Implement retry/backoff and basic logging; caller code assumes synchronous call-and-parse semantics.
- When expecting JSON from the model, prefer schema-first prompts (see `signals.py`) and validate with `jsonschema` if available.
- Use `sample_inputs/` for small fixtures (e.g., `01_macro_regime_classifier/sample_inputs`) when writing tests.
- There are currently no test/CI files in the repo — when adding functionality, create small unit tests that mock `call_llm` responses (pytests) to ensure deterministic behavior.

## What to avoid ❌
- Don't change prompt text lightly — small wording changes can change model behavior. If you do change prompts, add tests that assert expected parseable outputs.
- Do not commit API keys or sensitive configuration.

## When you change anything here ✍️
- Update `02_asset_allocation_signals/schema.json` when you change signal shape.
- Add/adjust unit tests that mock `llm_client.call_llm` and verify parsing, schema validity, and confidence ranges.

---

If anything is missing or unclear, say which behavior or file you'd like expanded and I will iterate. Thank you!