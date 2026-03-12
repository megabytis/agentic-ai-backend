## Contextual Retrieval

**What is it?**
A preprocessing step that uses an LLM to **add missing context** to each chunk before embedding/searching.

### The Problem:

When you chunk a document, each chunk loses its **place in the larger document**:

```
Original Document:
┌─────────────────────────────────────┐
│ Section 1: Intro                    │
│ ...                                 │
├─────────────────────────────────────┤
│ Section 2: Software Engineering     │ ← This chunk alone doesn't know
│ ... mentions INC-2023 ...           │   it's in a 10-section report,
├─────────────────────────────────────┤   or that other sections also
│ Section 10: Cybersecurity           │   mention the same incident
│ ... also mentions INC-2023 ...      │
└─────────────────────────────────────┘
```

### The Solution:

**Step 1: Add Context to Each Chunk**

```
Original Chunk: "The team resolved INC-2023 by patching the memory leak..."

+ LLM-generated context:
  "This is from Section 2 (Software Engineering) of a 10-section annual report.
   The same incident INC-2023 is also discussed in Section 10 (Cybersecurity)."

= Contextualized Chunk (store this instead):
  "[Context: This is from Section 2 (Software Engineering)...]
   The team resolved INC-2023 by patching the memory leak..."
```

### Why It Works:

| Before Context                           | After Context                                |
| ---------------------------------------- | -------------------------------------------- |
| Chunk mentions "INC-2023" but no context | Knows it's from Software Engineering section |
| Multiple sections mention same incident  | Each chunk knows about the relationship      |
| Chunk isolated from document structure   | Understands its place in the whole           |

### When to Use:

| Document Type                               | Contextual Retrieval Benefit        |
| ------------------------------------------- | ----------------------------------- |
| **Long reports** with interrelated sections | High - helps connect related chunks |
| **Technical docs** with cross-references    | High - preserves relationship info  |
| **Simple, standalone chunks**               | Low - context doesn't add much      |
| **Very large docs**                         | Use smart context selection         |

### Trade-offs:

| Pros                         | Cons                             |
| ---------------------------- | -------------------------------- |
| Preserves document structure | Extra LLM calls (cost/time)      |
| Connects related chunks      | More complex pipeline            |
| Better retrieval accuracy    | Need to manage context selection |
| Helps with ambiguous chunks  | May add redundant info           |

> **_So, Contextual retrieval fixes the "lost context" problem in chunking by having an LLM add back the missing document structure information before embedding. Especially useful for complex documents with interrelated sections._**
