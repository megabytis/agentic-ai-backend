## Introduction to RAG

**What is RAG?**
Retrieval Augmented Generation = Giving LLMs access to external knowledge by retrieving relevant documents/passages and including them in the prompt.

### The Problem:

- LLMs have knowledge cutoffs (don't know recent info)
- Can't access your private documents
- Limited context windows
- Expensive to put entire documents in prompts

### Two Approaches:

**Option 1: Stuff Everything in Prompt** ❌

- Put entire document / document's text in prompt
- Problems:
  - Context window limits i.e. if the document would be very very long then due to limit the model won't take it .
  - Model gets confused by too much info
  - Expensive and slow
  - Doesn't scale to multiple/large documents

**Option 2: RAG** ✅

1. **Preprocessing**: Split documents into chunks
2. **Retrieval**: Find chunks relevant to user's question
3. **Generation**: Put ONLY relevant chunks + question in prompt

### RAG Workflow:

```
Documents → Chunk → Store chunks
                    ↓
User Question → Find Relevant Chunks → Prompt (Relevant chunks + Question) → LLM → Answer
```

### Pros & Cons:

| ✅ Advantages                  | ❌ Challenges                   |
| ------------------------------ | ------------------------------- |
| Scales to large docs           | More complex to implement       |
| Lower cost (smaller prompts)   | Need chunking strategy          |
| Faster responses               | Need retrieval mechanism        |
| Can use multiple documents     | May miss context between chunks |
| Model focuses on relevant info | Need to define "relevance"      |

### Key Decisions You'll Need to Make:

1. **Chunking strategy** - How to split documents?
2. **Retrieval method** - How to find relevant chunks?
3. **Number of chunks** - How many to include?
4. **Context preservation** - How to maintain flow between chunks?

**Bottom line:** RAG is essential for working with large documents or private knowledge. It's more work to implement but necessary for production apps.
