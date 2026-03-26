## Defining Prompts in MCP

**What are Prompts?**
Pre-written, well-tested prompts that MCP servers can expose to clients. They're like **templates** for common tasks.

---

### Prompts vs Tools vs Resources:

| Feature       | Purpose                  | Example                            |
| ------------- | ------------------------ | ---------------------------------- |
| **Tools**     | Perform actions          | `edit_document`, `send_email`      |
| **Resources** | Provide data             | Document list, user profile        |
| **Prompts**   | Pre-written instructions | "Format this document in markdown" |

---

### The Use Case:

**Without Prompts (user writes):**

```
User: "Convert report.pdf to markdown format"
Claude: (does it, but prompt is generic)
Result: Okay, but could be better
```

**With Prompts (server provides optimized prompt):**

```
User: "/format report.pdf"
Server sends pre-written, tested prompt:
"You are a document formatter...
 Use markdown headings, lists, emphasis...
 Step 1: Read the document
 Step 2: Apply markdown
 Step 3: Update the document"

Result: Much better formatting!
```

---

### Defining a Prompt in MCP Server:

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("Document Server")

@mcp.prompt(
    name="format",
    description="Rewrite document in Markdown format"
)
def format_document(doc_id: str):
    """
    Args:
        doc_id: ID of the document to format
    """
    # Pre-written, well-tested prompt
    prompt_text = f"""
You are a document formatting assistant.
Format the document with ID: {doc_id}

Follow these steps:
1. Read the document using the read_document tool
2. Convert it to markdown with:
   - Proper headings (#, ##, ###)
   - Bullet points and numbered lists
   - Emphasis where appropriate
3. Update the document with the formatted version
4. Confirm the changes

Use the read_document and edit_document tools.
"""

    # Return as a message list
    return [
        base.UserMessage(prompt_text)
    ]
```

---

### How It Works:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User types "/format" in CLI                              │
│    ↓                                                        │
│ 2. Client detects slash command                             │
│    ↓                                                        │
│ 3. Client asks server: "What prompts do you have?"          │
│    ↓                                                        │
│ 4. Server returns: ["format"]                               │
│    ↓                                                        │
│ 5. Client shows autocomplete                                │
│    ↓                                                        │
│ 6. User selects "format" and enters doc_id                  │
│    ↓                                                        │
│ 7. Client calls: get_prompt("format", doc_id="report.pdf")  │
│    ↓                                                        │
│ 8. Server returns the pre-written prompt with doc_id filled │
│    ↓                                                        │
│ 9. Client sends prompt to Claude                            │
│    ↓                                                        │
│10. Claude executes (reads doc, formats, updates)            │
└─────────────────────────────────────────────────────────────┘
```

---

### Why Prompts Matter:

| Without Prompts            | With Prompts                     |
| -------------------------- | -------------------------------- |
| User must know what to ask | User types simple `/command`     |
| Generic prompting          | Specialized, tested prompts      |
| Inconsistent results       | Consistent, high-quality results |
| Every user figures it out  | Best practices built-in          |

---

### Implementation Pattern:

```python
@mcp.prompt(
    name="command_name",
    description="What this command does"
)
def command_name(param1: str, param2: int = 5):
    # Pre-written, optimized prompt
    prompt = f"""
    Specialized instructions...
    With parameters: {param1}, {param2}
    """
    return [base.UserMessage(prompt)]
```

---

### Key Takeaways:

1. **Prompts are pre-written templates** - Server authors write them once
2. **Well-tested** - Server authors optimize and eval them
3. **Client just calls** - User types `/command` and client sends the prompt
4. **Reduces user effort** - No need to craft perfect prompts
5. **Consistent quality** - Same prompt for everyone

**Bottom line:** Prompts let MCP servers provide **optimized, tested instructions** for common tasks, so users don't have to figure out the best way to ask! 🚀
