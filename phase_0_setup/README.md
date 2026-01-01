# Phase 0 — Setup & Mental Model

## Goal
Build a minimal GenAI backend that calls an LLM API and understand foundational concepts.

## What I Built
A Python script that:
- Takes user input
- Calls Gemini API
- Returns response + token usage

## Key Learnings
- Tokens are subword units (~4 chars each)
- Context window limits input + output size
- Models are stateless (no memory between calls)
- LLMs predict next tokens, not "think"

## Tech Stack
- Python 3.x
- google-genai SDK
- Gemini 2.5 Flash (free tier)

## How to Run
```bash
cd phase_0_setup/project
python main.py
```

## Next Phase
Phase 1: Prompting & Control