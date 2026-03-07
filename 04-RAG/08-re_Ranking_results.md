## Reranking Results

**What is Reranking?**
A post-processing step that uses an LLM to **reorder** our initial search results for better relevance.

### The Problem It Solves:

```
Query: "What did the ENG team do with incident 2023?"

Hybrid Search Results (before reranking):
1. Section 10 (Cybersecurity) - mentions incident
2. Section 2 (Software Engineering) - mentions incident + engineering

❌ Most relevant section (#2) is second!
```

### Reranking Flow:

```
User Query
    ↓
┌─────────────────────┐
│  Hybrid Search      │
│  (BM25 + Semantic)  │
└──────────┬──────────┘
           ↓
    [Initial Results: 10, 2, 5, 7, 3]
           ↓
┌─────────────────────┐
│  Reranker (LLM)     │
│  "Reorder by relevance"│
└──────────┬──────────┘
           ↓
    [Reranked Results: 2, 10, 5, 7, 3]  ✅
           ↓
    Send top_k to final prompt
```

### How It Works (with Document IDs):

```python
# 1. Assign IDs to chunks
chunks_with_ids = [
    {"id": "doc_001", "content": "Section 2: Software Engineering..."},
    {"id": "doc_002", "content": "Section 10: Cybersecurity..."},
    # ...
]

# 2. Reranker prompt
reranker_prompt = f"""
User Question: {query}

Here are documents that might be relevant.
Rank them by relevance (most relevant first).
Return ONLY the IDs in order as a JSON array.

Documents:
<document id="doc_001">
{chunk_1_content[:500]}...
</document>

<document id="doc_002">
{chunk_2_content[:500]}...
</document>

<!-- more documents... -->

Return format: ["doc_001", "doc_003", "doc_002", ...]
"""

# 3. LLM returns ordered IDs
response = llm_completion(reranker_prompt)
ordered_ids = json.loads(response)  # ["doc_002", "doc_001", ...]

# 4. Reorder your chunks
reranked_chunks = [id_to_chunk[id] for id in ordered_ids]
```

### Why Use IDs Instead of Full Text?

| Approach           | Problem                                  |
| ------------------ | ---------------------------------------- |
| Return full chunks | LLM copies huge text → slow, expensive   |
| Return IDs         | LLM returns small JSON → fast, efficient |

### Trade-offs:

| Advantages                   | Disadvantages                      |
| ---------------------------- | ---------------------------------- |
| Higher accuracy              | Increased latency (extra LLM call) |
| Fixes edge cases             | Extra cost                         |
| LLM understands nuance       | More complex pipeline              |
| Can catch what search missed | Need to manage IDs                 |

**Bottom line:** Reranking adds accuracy at the cost of speed. Use it when you need the absolute best relevance and can afford the extra LLM call.
