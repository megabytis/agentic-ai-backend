## Optimizing RAG Performance - What We Can Tune

### The 5 Key Areas to Optimize:

```
[RAG System] = Chunking → Embeddings → Search → Retrieval → Prompt
                    ↑          ↑         ↑         ↑         ↑
                 Tune 1      Tune 2    Tune 3    Tune 4    Tune 5
```

---

## **Tuning Area 1: Chunking Strategy**

| Parameter         | What It Does           | Typical Values                         | Impact                                                                           |
| ----------------- | ---------------------- | -------------------------------------- | -------------------------------------------------------------------------------- |
| **Chunk Size**    | How big each piece is  | 256, 512, 1024 tokens                  | Too small = loses context<br>Too big = includes noise                            |
| **Chunk Overlap** | Context between chunks | 10-20% of chunk size                   | Higher = more context, more duplication                                          |
| **Chunk Method**  | How you split          | character, sentence, section, semantic | Structure-based = best for structured docs<br>Semantic = best for varied content |

**Rule of Thumb:** Start with 512 tokens, 10% overlap, adjust based on your documents

---

## **Tuning Area 2: Embedding Model**

| Parameter        | What It Does               | Options                                              | Trade-off                                            |
| ---------------- | -------------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
| **Model Size**   | Dimension of vectors       | Small (384), Medium (768), Large (1536)              | Larger = more accurate, slower, more memory          |
| **Model Type**   | Domain-specific vs general | General (BGE, Ada), Domain-specific (medical, legal) | Domain models = better for specialized content       |
| **Quantization** | Compress vectors           | Float32, Float16, Int8                               | Lower precision = smaller DB, slightly less accuracy |

**Free Options:**

- `BAAI/bge-small-en-v1.5` (384 dim) - Fast, good for learning
- `BAAI/bge-base-en-v1.5` (768 dim) - Better accuracy
- `BAAI/bge-large-en-v1.5` (1024 dim) - Best accuracy, slower

---

## **Tuning Area 3: Search Algorithm**

| Parameter             | What It Does                 | Options                                    | When to Use                                                           |
| --------------------- | ---------------------------- | ------------------------------------------ | --------------------------------------------------------------------- |
| **Search Type**       | How you find matches         | Semantic only, Hybrid (semantic + keyword) | Hybrid = best for most cases<br>Semantic = when meaning > exact words |
| **Similarity Metric** | How you measure closeness    | Cosine, Euclidean, Dot Product             | Cosine = most common, works well                                      |
| **Top-K**             | Number of chunks to retrieve | 3, 5, 10                                   | Higher = more context, more noise                                     |

**Hybrid Search Formula:**

```python
final_score = (0.7 * semantic_score) + (0.3 * keyword_score)
# Adjust weights based on your data!
```

---

## **Tuning Area 4: Retrieval Parameters** 🎯

| Parameter                | What It Does                   | Typical Values                      | Effect                                     |
| ------------------------ | ------------------------------ | ----------------------------------- | ------------------------------------------ |
| **Similarity Threshold** | Minimum score to include       | 0.7, 0.8                            | Higher = fewer but more relevant chunks    |
| **Diversity Penalty**    | Avoid similar chunks           | MMR (Maximal Marginal Relevance)    | Prevents getting 3 nearly identical chunks |
| **Metadata Filtering**   | Filter by document type/source | date > 2024, category = "technical" | Reduces search space, improves relevance   |

**MMR (Diversity) Example:**

```python
# Without MMR: Gets 3 chunks all about "revenue"
# With MMR: Gets 1 revenue, 1 engineering, 1 customers
```

---

## **Tuning Area 5: Prompt Engineering** 📝

| Parameter               | What It Does               | Example                            | Impact                                           |
| ----------------------- | -------------------------- | ---------------------------------- | ------------------------------------------------ |
| **Context Window**      | How many chunks to include | "Use these 3 sources..."           | More = comprehensive, but model may get confused |
| **Instruction Clarity** | How to use the context     | "Answer ONLY from the context"     | Clear instructions = better responses            |
| **Output Format**       | Structure of answer        | "Bullet points", "JSON", "Summary" | Consistent format = easier to parse              |

**Prompt Template Evolution:**

```python
# Basic
prompt = f"Context: {context}\nQuestion: {question}"

# Better
prompt = f"""Answer based ONLY on this context:
{context}

Question: {question}
If answer not in context, say "I don't know".
"""

# Best
prompt = f"""CONTEXT (from official documents):
{context}

QUESTION: {question}

INSTRUCTIONS:
1. Only use information from the context
2. If unsure, say "I cannot find this information"
3. Quote relevant parts when possible
4. Keep answer concise

ANSWER:"""
```

---

## Optimization Checklist ✅

### Start Here (Beginner):

- [ ] Adjust chunk size (256 → 512 → 1024)
- [ ] Change top-K (3 → 5 → 10)
- [ ] Add overlap (10% → 20%)

### Intermediate:

- [ ] Try different embedding models
- [ ] Implement similarity threshold
- [ ] Add metadata filtering

### Advanced:

- [ ] Hybrid search (semantic + keyword)
- [ ] MMR for diversity
- [ ] Query expansion (generate multiple query versions)
- [ ] Reranking with cross-encoder

---

## Real-World Example: Tuning Journey

```python
# Version 1 (Basic)
chunk_size = 512
top_k = 3
similarity = cosine
# Accuracy: 65%

# Version 2 (After tuning)
chunk_size = 768
top_k = 5
similarity_threshold = 0.75
use_hybrid = True
# Accuracy: 82%

# Version 3 (Optimized)
chunk_size = 1024
overlap = 150
top_k = 7
similarity_threshold = 0.7
use_hybrid = True
mmr_lambda = 0.5
rerank = True
# Accuracy: 91%
```

---

## The 30-Second Summary ⏱️

```
To optimize RAG, tune these in order:

1. Chunk size & overlap (get the pieces right)
2. Top-K & threshold (get the right number of pieces)
3. Embedding model (get better quality pieces)
4. Hybrid search & diversity (get varied pieces)
5. Prompt (use the pieces well)

REMEMBER: Start simple, measure, then tune one thing at a time!
```
