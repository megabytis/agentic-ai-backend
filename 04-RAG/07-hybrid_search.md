Hybrid Search

Now **combining BM25 (lexical) + Semantic Search (embeddings)** into a single hybrid search system.

### The Hybrid Search Flow:

```
User Query
     ↓
┌─────────────┬─────────────┐
↓             ↓             ↓
BM25 Search   Semantic Search   (maybe others)
↓             ↓             ↓
[Results A]   [Results B]
     ↓             ↓
┌─────────────┬─────────────┐
     ↓             ↓
   Merge & Rerank Results
     ↓
┌─────────────────────────┐
│ Top K Combined Chunks   │
│ 1. Section 2 (BM25 #1)  │
│ 2. Section 6 (Semantic) │
│ 3. Section 5 (BM25 #2)  │
└─────────────────────────┘
     ↓
   Send to LLM
```

### Why Combine Both?

| Search Type  | Strengths                        | Weaknesses                   |
| ------------ | -------------------------------- | ---------------------------- |
| **BM25**     | Exact matches, rare terms, IDs   | Misses synonyms, meaning     |
| **Semantic** | Finds related concepts, synonyms | Can miss specific rare terms |
| **Hybrid**   | ✅ Best of both worlds           | Slightly more complex        |

### More Sophisticated Approaches:

1. **Reciprocal Rank Fusion (RRF)** - Standard formula for merging search results
2. **Learned weighting** - Train a model to weight each search type
3. **Query analysis** - Decide which search to use based on query type

**Bottom line:** Hybrid search gives you the precision of BM25 + the understanding of semantic search. Next video will likely show implementing this merge!
