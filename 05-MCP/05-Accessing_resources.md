## Accessing Resources

**What This Shows:** How the client requests and processes data from MCP server resources.

---

### The Client Side Implementation:

```python
import json
from pydantic import AnyUrl

class MCPClient:
    async def read_resource(self, uri: str):
        """Fetch a resource from the MCP server"""

        # 1. Request resource from server
        result = await self.session.read_resource(AnyUrl(uri))

        # 2. Get the first content block
        resource = result.contents[0]

        # 3. Parse based on MIME type
        if resource.mime_type == "application/json":
            # JSON data → parse and return as dict
            return json.loads(resource.text)
        else:
            # Plain text → return as is
            return resource.text
```

---

### Why This Matters:

**The server returns structured data:**

```python
# Server side (what we built earlier)
@mcp.resource("docs://documents", mime_type="application/json")
def list_documents():
    return ["report.pdf", "notes.txt"]  # Returns list

# Client receives:
{
    "contents": [{
        "mime_type": "application/json",
        "text": '["report.pdf", "notes.txt"]'  # Stringified JSON!
    }]
}
```

**Client must parse:**

```python
# Raw from server: string
'["report.pdf", "notes.txt"]'

# After parsing: usable list
["report.pdf", "notes.txt"]
```

---

### The Complete Flow:

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. User types "@"                                               │
│    ↓                                                            │
│ 2. Client detects mention                                       │
│    ↓                                                            │
│ 3. Client calls read_resource("docs://documents")              │
│    ↓                                                            │
│ 4. Server returns list of documents as JSON string             │
│    ↓                                                            │
│ 5. Client parses JSON into list                                 │
│    ↓                                                            │
│ 6. Client shows autocomplete options                            │
│    ↓                                                            │
│ 7. User selects "report.pdf"                                    │
│    ↓                                                            │
│ 8. Client calls read_resource("docs://documents/report.pdf")   │
│    ↓                                                            │
│ 9. Server returns document content as plain text                │
│    ↓                                                            │
│10. Client injects content into prompt                          │
│    ↓                                                            │
│11. Send to Claude (no tool call needed!)                       │
└─────────────────────────────────────────────────────────────────┘
```

---

### Key Points:

| Aspect        | Details                                               |
| ------------- | ----------------------------------------------------- |
| **URI**       | Unique identifier for the resource (like a URL)       |
| **MIME Type** | Tells client how to parse the data (JSON, text, etc.) |
| **Contents**  | Server returns list of content blocks (usually one)   |
| **Parsing**   | Client must parse based on MIME type                  |

---

### In Future Projects:

```python
# we'll write code like this:
class MCPClient:
    async def list_documents(self):
        # Call the static resource
        return await self.read_resource("docs://documents")

    async def get_document(self, doc_id: str):
        # Call the templated resource
        return await self.read_resource(f"docs://documents/{doc_id}")

# Then in your app:
docs = await client.list_documents()  # ["report.pdf", ...]
content = await client.get_document("report.pdf")  # "The report says..."
```

---

### Bottom Line:

**Resources = Server provides data**  
**Client = Parses and uses that data**

The client's `read_resource` function:

1. Sends request with URI
2. Gets response with data + MIME type
3. Parses based on MIME type
4. Returns usable data to your app

**That's it!** Resources are just data endpoints your client can read. 🚀
