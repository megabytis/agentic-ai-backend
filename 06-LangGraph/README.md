# LangGraph Complete Curriculum

## Module 1: Introduction

- Motivation (why LangGraph vs if-else, vs chains)
- What is a graph (node, edge, flow)
- Graph types (linear, branching, cyclic)
- Entry point, termination, loops
- Visual flow of graphs (step-by-step execution)
- Simple graph mental model
- LangGraph overview (what it is / not)
- Chains vs Graphs
- Router concept (conditional edges)
- Agent concept (decision-making system)
- Agent with memory (intro to state)
- Observability concept (LangSmith)

## Module 2: State and Memory

- What is state (core concept)
- State as shared data (mental model)
- State lifecycle (creation → update → usage)
- State schema (structure, types)
- Default values in state
- State mutation vs immutability
- Reducers (how state updates)
- Merge conflicts / bad state updates
- State flow across nodes (visualized)
- Multiple schemas
- Message trimming/filtering
- Short-term memory
- External memory concept

## Module 3: UX and Human-in-the-Loop

- Streaming (real-time output flow)
- Breakpoints (pause/resume execution flow)
- Human feedback (editing state)
- Dynamic routing based on user input
- Interrupts and resumption
- Time travel (checkpoint + rollback)
- Execution tracing and debugging flow

## Module 4: Building Systems

- Parallel execution (how multiple nodes run)
- Subgraphs (graph inside node)
- Map-reduce pattern (with flow breakdown)
- Multi-agent systems (interaction flow)
- Error handling (retry, fallback paths)
- System flow design thinking (end-to-end graph)

## Module 5: Long-Term Memory

- Short vs long-term memory
- Persistent memory (storage concept)
- Memory schema design
- Profile vs collection memory
- State persistence across sessions
- Agent with long-term memory
- Memory retrieval flow

## Module 6: Deployment

- Deployment concepts
- Backend architecture thinking
- LangGraph in real backend systems
- API integration flow
- Async systems & double texting flow
- Assistant APIs
- End-to-end request lifecycle
