## Prompts in the Client

**What This Shows:** How the client requests prompts from the MCP server and uses them.

---

### Client Side Implementation:

```python
class MCPClient:
    async def list_prompts(self):
        """Get all available prompts from server"""
        result = await self.session.list_prompts()
        return result.prompts  # List of prompt names

    async def get_prompt(self, prompt_name: str, arguments: dict):
        """Get a specific prompt with arguments filled in"""
        result = await self.session.get_prompt(prompt_name, arguments)
        return result.messages  # Ready-to-use messages
```

---

### How It Works Together:

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. User types "/" in CLI                                        │
│    ↓                                                            │
│ 2. Client calls: list_prompts()                                 │
│    ↓                                                            │
│ 3. Server returns: ["format"]                                   │
│    ↓                                                            │
│ 4. Client shows autocomplete: "format"                          │
│    ↓                                                            │
│ 5. User selects "format" and picks document "plan.md"          │
│    ↓                                                            │
│ 6. Client calls: get_prompt("format", {"doc_id": "plan.md"})   │
│    ↓                                                            │
│ 7. Server returns:                                              │
│    [{"role": "user", "content": "Format plan.md in markdown..."}]│
│    ↓                                                            │
│ 8. Client sends these messages directly to Claude              │
│    ↓                                                            │
│ 9. Claude executes (reads doc, formats, updates)               │
└─────────────────────────────────────────────────────────────────┘
```

---

### The Complete Prompt Flow:

```python
# Server side (we already built)
@mcp.prompt(name="format", description="Format document in markdown")
def format_document(doc_id: str):
    prompt = f"Format document {doc_id} in markdown..."
    return [base.UserMessage(prompt)]

# Client side (we just added)
async def get_prompt(self, name: str, args: dict):
    result = await self.session.get_prompt(name, args)
    return result.messages  # ["Format document plan.md..."]

# In your app (already implemented)
if command == "/format":
    messages = await client.get_prompt("format", {"doc_id": "plan.md"})
    response = await claude.chat(messages)  # Send directly to Claude
```

---

### Key Points:

| Function         | What It Does                                       |
| ---------------- | -------------------------------------------------- |
| `list_prompts()` | Gets available prompts (for autocomplete)          |
| `get_prompt()`   | Fills template with arguments and returns messages |

---

### Why This Pattern:

1. **Separation of concerns**
   - Server: Defines prompt templates
   - Client: Just requests and uses them

2. **Dynamic**
   - Client can get prompts at runtime
   - No hardcoded prompt list in client

3. **Flexible**
   - Add new prompts without changing client
   - Server evolves independently

---

### The Big Picture:

```
┌─────────────────┐         ┌─────────────────┐
│   MCP Server    │         │   MCP Client    │
├─────────────────┤         ├─────────────────┤
│ @prompt(name)   │◄─────── │ list_prompts()  │
│   format doc    │         │ get_prompt()    │
└─────────────────┘         └─────────────────┘
        │                          │
        │                          ▼
        │                   ┌─────────────────┐
        │                   │     Claude      │
        │                   └─────────────────┘
        │
        ▼
┌─────────────────┐
│   User Types    │
│   "/format"     │
└─────────────────┘
```

---

### Bottom Line:

**Client's role in prompts:**

1. Ask server for available prompts (`list_prompts`)
2. Get filled prompt with user's arguments (`get_prompt`)
3. Send messages to Claude

**That's it!** Client is just a messenger - server does the heavy lifting of defining and testing the prompts. 🚀
