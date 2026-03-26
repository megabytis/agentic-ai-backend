## Implementing an MCP Client

### The Client's Job:

```
 Our App (Client)  →  MCP Server
     ↓                    ↓
   Ask for tools      Provides tools
     ↓                    ↓
   Call tools         Executes tools
```

---

### Key Code Patterns:

**1. List Tools (Get available tools from server):**

```python
async def list_tools(self):
    result = await self.session.list_tools()
    return result.tools
```

**2. Call Tool (Execute a tool on server):**

```python
async def call_tool(self, tool_name, tool_input):
    return await self.session.call_tool(tool_name, tool_input)
```

---

### Why Wrap in a Class?

```python
class MCPClient:
    def __init__(self):
        self.session = None  # Connection to server

    async def connect(self):
        # Start server process
        # Create session
        # Clean up resources on close

    async def list_tools(self):
        return await self.session.list_tools()

    async def call_tool(self, name, args):
        return await self.session.call_tool(name, args)

    async def cleanup(self):
        # Close connection properly
```

**Why?** Resource management (start/stop server, clean up)

---

### Complete Client Flow:

```python
# 1. Create client
client = MCPClient()

# 2. Connect to server
await client.connect()

# 3. Get tools for Claude
tools = await client.list_tools()

# 4. Send to Claude
response = await claude.chat(query, tools)

# 5. If Claude wants to use a tool:
if response.tool_calls:
    for call in response.tool_calls:
        # Execute via MCP server (not locally!)
        result = await client.call_tool(call.name, call.arguments)

# 6. Send result back to Claude for final answer
```

---

### What This Means :

| We Write            | Someone Else Writes      |
| ------------------- | ------------------------ |
| `list_tools()` call | The actual tools         |
| `call_tool()` call  | The tool implementation  |
| Connection logic    | MCP SDK handles it       |
| Cleanup code        | Server handles execution |

---

### The Key Insight:

**Our client code is simple:**

- Connect to server
- Get tools
- Call tools when Claude asks

**We don't write:**

- Tool implementations
- API calls
- Error handling for external services

---
