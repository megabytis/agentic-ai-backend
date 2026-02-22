## Text Chunking Strategies

**Why Chunking Matters:** How you split documents directly impacts RAG quality. Bad chunking = wrong context retrieved = wrong answers.

### The Problem Example:

```
Document:
## Medical Research
... bugs in clinical trials ... infection vectors ...

## Software Engineering
... fixed 42 bugs ... infection vectors in code ...
```

If user asks: _"How many bugs did engineers fix?"_

Bad chunking (by line) might retrieve the medical "bugs" chunk instead of the software engineering chunk, giving completely wrong context.

---

### Three Main Chunking Strategies

| Strategy            | How It Works                            | Pros                                                                                             | Cons                                                                                |
| ------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| **Size-Based**      | Split into equal character/token chunks | • Simplest to implement<br>• Works for any document<br>• Most common in production               | • Cuts words/sentences<br>• Loses context<br>• Needs overlap                        |
| **Structure-Based** | Split by headers, sections, paragraphs  | • Preserves document structure<br>• Each chunk has clear context<br>• Best quality when possible | • Requires structured docs<br>• Hard with PDFs/plain text<br>• Not always available |
| **Semantic-Based**  | Group related sentences using NLP       | • Contextually coherent chunks<br>• Adapts to content                                            | • Complex to implement<br>• Slower processing<br>• Overkill for many cases          |

---

### Size-Based with Overlap

**Basic size-based** (no overlap):

```
Chunk 1: "The company reported significant"
Chunk 2: "t growth in Q3 with revenues..."
```

❌ Problem: "significant" cut off, loses meaning

**With overlap** (include text from neighbors):

```
Chunk 1: "The company reported significant growth in Q3..."
Chunk 2: "significant growth in Q3 with revenues increasing..."
```

✅ Better: Each chunk has context, though some duplication

---

### Which Strategy to Choose?

| Document Type                          | Best Strategy                         |
| -------------------------------------- | ------------------------------------- |
| Markdown/HTML with clear headers       | **Structure-based**                   |
| Well-written prose (articles, reports) | **Sentence-based**                    |
| PDFs without structure                 | **Size-based with overlap**           |
| Code                                   | **Size-based** (sentences don't work) |
| Mixed/unpredictable formats            | **Size-based** (fallback)             |

---

### Key Takeaways

1. **No single best strategy** - depends on your documents
2. **Start simple** - size-based with overlap works for most cases
3. **Test different chunk sizes** - too small loses context, too large includes noise
4. **Overlap helps** - 10-20% overlap preserves context between chunks
5. **Structure is gold** - if your docs have it, use it

**Bottom lines:**

- Chunking is a critical design decision in RAG. We'll need to choose based on our specific documents and use case.

- BTW in porduction, we'll use tools like LangChain, LlamaIndex that have built-in tools for chunking

- So, know the concepts, not the code. You can always look up implementations when needed.
