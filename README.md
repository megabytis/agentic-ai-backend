## Directories Structure

```text
agentic-ai-backend/
├── README.md
├── .gitignore
├── .env.example
├── pyproject.toml
├── .python-version
├── Makefile
│
├── docs/
│   ├── architecture/
│   │   ├── system_overview.md
│   │   ├── ai_backend_basics.md
│   │   └── production_ai_backend.md
│   │
│   ├── decisions/
│   │   ├── why_python.md
│   │   ├── why_fastapi.md
│   │   ├── why_langgraph.md
│   │   ├── why_rag.md
│   │   └── why_not_finetuning.md
│   │
│   ├── mental_models/
│   │   ├── llm_statelessness.md
│   │   ├── tokens_and_context.md
│   │   ├── prompting_vs_programming.md
│   │   ├── agents_vs_workflows.md
│   │   └── tool_calling_loop.md
│   │
│   ├── glossary.md
│   └── roadmap.md
│
├── shared/
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── client.py
│   │   └── models.py
│   │
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── system_prompts.py
│   │   ├── user_prompts.py
│   │   └── guardrails.py
│   │
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── buffer_memory.py
│   │   └── summary_memory.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── registry.py
│   │   ├── schemas.py
│   │   └── executor.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   └── pipeline.py
│   │
│   ├── observability/
│   │   ├── __init__.py
│   │   ├── logging.py
│   │   ├── tracing.py
│   │   └── cost_tracking.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── base.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       └── helpers.py
│
├── phases/
│   ├── phase_00_setup/
│   │   ├── README.md
│   │   ├── concepts.md
│   │   ├── decisions.md
│   │   ├── app/
│   │   │   └── main.py
│   │   └── notes.md
│   │
│   ├── phase_01_prompting/
│   │   ├── README.md
│   │   ├── concepts.md
│   │   ├── decisions.md
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── prompt_controller.py
│   │   │   └── prompts.py
│   │   └── notes.md
│   │
│   ├── phase_02_memory/
│   │   ├── README.md
│   │   ├── concepts.md
│   │   ├── decisions.md
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   └── memory_service.py
│   │   └── notes.md
│   │
│   ├── phase_03_structured_output/
│   │   ├── README.md
│   │   ├── concepts.md
│   │   ├── decisions.md
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   └── schemas.py
│   │   └── notes.md
│   │
│   ├── phase_04_tool_calling/
│   │   ├── README.md
│   │   ├── concepts.md
│   │   ├── decisions.md
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── tools.py
│   │   │   └── agent_loop.py
│   │   └── notes.md
│   │
│   ├── phase_05_rag/
│   │   ├── README.md
│   │   ├── concepts.md
│   │   ├── decisions.md
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   └── rag_service.py
│   │   └── notes.md
│   │
│   ├── phase_06_agentic_ai/
│   │   ├── README.md
│   │   ├── concepts.md
│   │   ├── decisions.md
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── planner.py
│   │   │   ├── executor.py
│   │   │   └── reflector.py
│   │   └── notes.md
│   │
│   ├── phase_07_langgraph/
│   │   ├── README.md
│   │   ├── concepts.md
│   │   ├── decisions.md
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── graph.py
│   │   │   └── nodes.py
│   │   └── notes.md
│   │
│   ├── phase_08_mcp/
│   │   ├── README.md
│   │   ├── concepts.md
│   │   ├── decisions.md
│   │   ├── app/
│   │   │   ├── server/
│   │   │   │   ├── main.py
│   │   │   │   └── resources.py
│   │   │   └── client/
│   │   │       └── main.py
│   │   └── notes.md
│   │
│   ├── phase_09_production/
│   │   ├── README.md
│   │   ├── concepts.md
│   │   ├── decisions.md
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── security.py
│   │   │   ├── observability.py
│   │   │   └── cost_control.py
│   │   └── notes.md
│   │
│   └── phase_10_portfolio/
│       ├── README.md
│       ├── ARCHITECTURE.md
│       ├── resume_notes.md
│       ├── interview_prep.md
│       └── demo_walkthrough.md
│
└── experiments/
    ├── README.md
    ├── prompt_playground/
    ├── token_limits/
    └── failure_cases/
```

# Agentic AI Backend

My journey learning GenAI engineering from zero to job-ready.

## Progress

- ✅ **Phase 0**: Setup & Mental Model (Week 1)
- ⬜ **Phase 1**: Prompting & Control (Week 2)
- ⬜ **Phase 2**: Memory & Context (Week 3)
- ⬜ **Phase 3**: Structured Outputs (Week 4)
- ⬜ **Phase 4**: Tool Calling (Week 5)
- ⬜ **Phase 5**: RAG (Week 6)
- ⬜ **Phase 6**: Agentic AI (Week 7)
- ⬜ **Phase 7**: LangGraph (Week 8)
- ⬜ **Phase 8**: MCP (Week 9)
- ⬜ **Phase 9**: Production Readiness (Week 10)
- ⬜ **Phase 10**: Portfolio & Hiring (Week 11-12)

## What I'm Learning

Building production-grade GenAI systems:
- AI-integrated backends
- RAG pipelines
- Tool-using agents
- Agentic workflows
- LangGraph
- MCP servers

## Tech Stack

- Python
- Google Gemini API
- LangGraph (later phases)
- Vector DBs (later phases)

## Repository Structure

Each phase has:
- `/project` - working code
- `/notes.md` - my explanations
- `README.md` - phase summary

## Current Phase

**Phase 0: Setup & Mental Model**

Built a minimal GenAI backend and learned:
- What tokens actually are
- Why context windows matter
- Why models are stateless
- What LLMs actually do