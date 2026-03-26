## Defining Resources in MCP

**What are Resources?**
MCP servers can expose **data** (not just actions/tools) through **resources**. Think of them as "read-only data endpoints" that the client can access.

---

### Resources vs Tools:

| Feature       | Tools                         | Resources                          |
| ------------- | ----------------------------- | ---------------------------------- |
| **Purpose**   | Perform actions               | Provide data                       |
| **Example**   | `edit_document`, `send_email` | `document_content`, `user_profile` |
| **When Used** | Claude decides                | Client pre-fetches                 |
| **Use Case**  | Write/update                  | Read-only access                   |

---

### Two Types of Resources:

**1. Direct/Static Resources** (fixed URI):

```python
@mcp.resource("docs://documents", mime_type="application/json")
def list_documents():
    """Returns list of all available document names"""
    return list(docs.keys())
```

- Always returns same structure
- URI doesn't change
- Good for: document lists, static configs

**2. Templated Resources** (with parameters):

```python
@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_document(doc_id: str):
    """Returns content of a specific document"""
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")
    return docs[doc_id]
```

- URI has placeholders `{param}`
- Parameter becomes function argument
- Good for: getting specific documents, user profiles

---

### Resource Flow:

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Client  │────▶│ Server  │────▶│  Data   │
│         │     │         │     │ Source  │
└─────────┘     └─────────┘     └─────────┘
     │               │                │
     │ ReadResource  │                │
     │─────────────▶ │                │
     │               │ Fetch Data     │
     │               │───────────────▶│
     │               │                │
     │               │ Return Result  │
     │               │◀───────────────│
     │               │                │
     │ ReadResource  │                │
     │ Result        │                │
     │◀───────────── │                │
```

---

### Why This Matters:

**Without Resources:**

```
User: @report.pdf → Client doesn't know it → Claude must call tool → Extra LLM call
```

**With Resources:**

```
User: @report.pdf → Client fetches via resource → Injects content → Claude answers directly
```

---

### Implementation Pattern:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Document Server")

# Static resource - always same data
@mcp.resource("docs://list", mime_type="application/json")
def list_docs() -> list:
    return ["report.pdf", "notes.txt", "readme.md"]

# Templated resource - parameterized access
@mcp.resource("docs://{doc_id}", mime_type="text/plain")
def get_doc(doc_id: str) -> str:
    return docs.get(doc_id, f"Document {doc_id} not found")
```

---

### Key Takeaways:

1. **Resources provide data** (read-only), Tools perform actions (write/modify)
2. **Two types**: Static (fixed URI) and Templated (with parameters)
3. **MIME types** hint to client what data format to expect
4. **Resources are pre-fetched** by client, not decided by Claude
5. **URI is like a route** - defines how to access the data

**Bottom line:** Resources let your client pre-load data that Claude might need, reducing tool calls and improving response time! 🚀
