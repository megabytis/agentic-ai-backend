## Directories Structure

```text
agentic-ai-backend/
├── README.md                          # Repo overview, progress tracker, navigation
├── .gitignore                         # Python, env, IDE files
├── requirements.txt                   # Global dependencies (minimal, updated per phase)
├── setup.py                           # Optional: for shared utils as package
│
├── docs/
│   ├── ARCHITECTURE.md                # High-level system design decisions
│   ├── LEARNINGS.md                   # Key insights, mistakes, aha moments
│   ├── GLOSSARY.md                    # Terms you learn (embeddings, tokens, etc.)
│   └── PHASE_NOTES/
│       ├── phase_0.md
│       ├── phase_1.md
│       ├── ...
│       └── phase_10.md
│
├── shared/
│   ├── __init__.py
│   ├── llm_client.py                  # Shared LLM wrapper (OpenAI/Anthropic)
│   ├── prompt_templates.py            # Reusable prompt structures
│   ├── config.py                      # Environment vars, API keys
│   └── utils.py                       # Common helpers (logging, validation)
│
├── phase_0_setup/
│   ├── README.md                      # Phase goal, concepts, project spec
│   ├── project/
│   │   ├── main.py                    # Minimal GenAI backend service
│   │   ├── requirements.txt           # Phase-specific deps
│   │   └── .env.example               # API key template
│   └── notes.md                       # Your written explanations
│
├── phase_1_prompting/
│   ├── README.md
│   ├── project/
│   │   ├── main.py                    # Prompt-controlled chatbot backend
│   │   ├── prompts.py                 # Prompt variations
│   │   └── tests.py                   # Manual test cases
│   └── notes.md
│
├── phase_2_memory/
│   ├── README.md
│   ├── project/
│   │   ├── main.py                    # Chat backend with memory
│   │   ├── memory.py                  # Memory strategies
│   │   └── tests.py
│   └── notes.md
│
├── phase_3_structured_outputs/
│   ├── README.md
│   ├── project/
│   │   ├── main.py                    # JSON output backend
│   │   ├── schemas.py                 # Pydantic models
│   │   └── tests.py
│   └── notes.md
│
├── phase_4_tool_calling/
│   ├── README.md
│   ├── project/
│   │   ├── main.py                    # AI agent with tools
│   │   ├── tools.py                   # Tool definitions
│   │   └── tests.py
│   └── notes.md
│
├── phase_5_rag/
│   ├── README.md
│   ├── project/
│   │   ├── main.py                    # Knowledge-base chatbot
│   │   ├── embeddings.py              # Embedding logic
│   │   ├── vectordb.py                # Vector store wrapper
│   │   ├── chunking.py                # Document chunking
│   │   ├── data/                      # Sample documents
│   │   └── tests.py
│   └── notes.md
│
├── phase_6_agentic/
│   ├── README.md
│   ├── project/
│   │   ├── main.py                    # Multi-step task agent
│   │   ├── agent.py                   # Agent logic (plan, execute, reflect)
│   │   ├── tools.py
│   │   └── tests.py
│   └── notes.md
│
├── phase_7_langgraph/
│   ├── README.md
│   ├── project/
│   │   ├── main.py                    # Graph-based workflow
│   │   ├── graph.py                   # LangGraph structure
│   │   ├── nodes.py                   # Node implementations
│   │   └── tests.py
│   └── notes.md
│
├── phase_8_mcp/
│   ├── README.md
│   ├── project/
│   │   ├── server/
│   │   │   ├── main.py                # MCP server
│   │   │   └── resources.py
│   │   ├── client/
│   │   │   └── main.py                # MCP client
│   │   └── tests.py
│   └── notes.md
│
├── phase_9_production/
│   ├── README.md
│   ├── project/
│   │   ├── main.py                    # Production-ready service
│   │   ├── observability.py           # Logging, tracing
│   │   ├── security.py                # Input validation, rate limiting
│   │   ├── cost_control.py            # Token tracking
│   │   └── tests.py
│   └── notes.md
│
├── phase_10_portfolio/
│   ├── README.md
│   ├── final_project/
│   │   ├── (structured like production service)
│   │   └── ARCHITECTURE.md            # Full system explanation
│   ├── resume_guide.md
│   ├── interview_prep.md
│   └── demo_script.md
│
└── experiments/                        # Scratch work, failed attempts, explorations
    └── README.md                       # What this folder is for
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