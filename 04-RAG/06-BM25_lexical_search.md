**What is BM25?**
A **lexical (keyword-based) search algorithm** that finds documents by matching actual words, not meaning. It's an improved version of TF-IDF.

### How It Works:

**BM25 considers:**

- **Term Frequency** - How often the word appears in the document (more = relevant)
- **Document Length** - Longer docs get normalized (a word in a short doc matters more)
- **Rare Words** - Uncommon terms get higher weight (e.g., "incident-2023" > "the")

### BM25 vs Semantic Search:

| Aspect            | BM25 (Lexical)                          | Embeddings (Semantic)        |
| ----------------- | --------------------------------------- | ---------------------------- |
| **Matches**       | Exact words                             | Meaning/concepts             |
| **Strengths**     | Rare terms, proper nouns                | Synonyms, related ideas      |
| **Weakness**      | Misses synonyms ("car" vs "automobile") | Can miss specific rare terms |
| **Example Query** | "incident-2023"                         | "recent problems"            |

### Why Both Matter:

**Without BM25:**

```
Query: "incident-2023 report"
Semantic search might find: "2023 security breach analysis" (good)
But might miss the exact document titled "incident-2023-summary.pdf"
```

**Without Semantic:**

```
Query: "car accidents"
BM25 finds docs with "car" and "accidents" but misses "automobile collisions"
```
