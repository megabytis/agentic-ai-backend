## Text Embeddings

**What is an Embedding?**
A **numerical representation** of text meaning - a long list of numbers (vectors) that captures the semantic content.

```
"I'm very happy today" → [0.82, -0.13, 0.45, 0.91, -0.32, ...] (768+ numbers)
```

### Key Concepts:

1. **What the numbers mean:**
   - Each number = "score" for some abstract quality (but we don't know what)
   - Think of it as: dimension 1 = "happiness", dimension 2 = "fruit-related", etc. (these labels are made up!)
   - Similar texts have similar numbers (vectors close together)

2. **How they're used in RAG:**
   - Generate embeddings for ALL text chunks (once, upfront)
   - Generate embedding for user question (on the fly)
   - Find chunks with embeddings **most similar** to question embedding
   - This is **semantic search** - finds meaning, not just keywords

### The Workflow:

```
Preprocessing:
Documents → Chunk → Generate Embeddings for all chunks → Store vectors

Query Time:
User Question → Generate Embedding → Find closest chunk vectors → Retrieve those chunks
```

### Embedding Providers:

| Provider                  | Model                    | Notes                                        |
| ------------------------- | ------------------------ | -------------------------------------------- |
| **Voyage AI**             | `voyage-2`               | Recommended with Claude, free tier available |
| **OpenAI**                | `text-embedding-3-small` | Popular, cheap                               |
| **Cohere**                | `embed-english-v3.0`     | Good for multilingual                        |
| **Sentence Transformers** | Various                  | Run locally (free, slower)                   |

### Simple Implementation:

```python
# Install: pip install voyageai
import voyageai

vo = voyageai.Client(api_key="your-api-key")

def get_embedding(text):
    result = vo.embed([text], model="voyage-2")
    return result.embeddings[0]  # Returns list of floats

# Example
chunk_text = "The company reported strong Q3 earnings..."
chunk_embedding = get_embedding(chunk_text)  # Store this

query = "How did the company perform last quarter?"
query_embedding = get_embedding(query)  # Generate at query time

# Then find closest chunks using cosine similarity
```

### Why This Matters:

- **Semantic understanding** - Finds "profit" when user asks "earnings"
- **Language agnostic** - Works across languages
- **Scales to millions** of chunks with vector databases

**Bottom line:** Embeddings convert text to numbers so we can do math to find meaning. The actual implementation is simple - the hard part is using them effectively in your RAG pipeline.
