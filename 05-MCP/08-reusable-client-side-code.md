## This Pattern Works for ANY MCP Server! 🎯

The pattern is **exactly the same** for every MCP server:

```python
# UNIVERSAL MCP PATTERN - Works for ANY server!
async with ClientSession(server_params) as session:
    # 1. Get tools (always works)
    tools = await session.list_tools()

    # 2. Get resources (if server has them)
    resources = await session.list_resources()

    # 3. Get prompts (if server has them)
    prompts = await session.list_prompts()

    # 4. Call any tool
    result = await session.call_tool("tool_name", {"arg": "value"})

    # 5. Read any resource
    data = await session.read_resource("resource_uri")

    # 6. Get any prompt
    prompt = await session.get_prompt("prompt_name", {"param": "value"})
```

---

### Different Servers, Same Code:

| MCP Server       | What You Change         | What Stays Same           |
| ---------------- | ----------------------- | ------------------------- |
| **filesystem**   | `args` path             | Everything else           |
| **fetch**        | Command to start server | Same pattern              |
| **git**          | Command to start server | Same pattern              |
| **brave-search** | Command + API key       | Same pattern              |
| **sqlite**       | Command + database path | Same pattern              |
| **ANY**          | Just the server startup | **Client code IDENTICAL** |

---

### Examples:

#### 1. Filesystem Server

```python
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/my/workspace"]
)
async with ClientSession(server_params) as session:
    tools = await session.list_tools()  # read_file, write_file, etc.
```

#### 2. Fetch Server (HTTP requests)

```python
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-fetch"]
)
async with ClientSession(server_params) as session:
    tools = await session.list_tools()  # fetch_url, etc.
    result = await session.call_tool("fetch_url", {"url": "https://api.github.com"})
```

#### 3. Git Server

```python
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-git", "/my/repo"]
)
async with ClientSession(server_params) as session:
    tools = await session.list_tools()  # git_status, git_log, git_commit
    result = await session.call_tool("git_status", {})
```

#### 4. Memory Server (Store/Recall)

```python
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-memory"]
)
async with ClientSession(server_params) as session:
    tools = await session.list_tools()  # create_entities, create_relations, query
    result = await session.call_tool("create_entities", {"entities": [...]})
```

#### 5. Multiple Servers at Once!

```python
# Connect to multiple MCP servers
async with ClientSession(filesystem_params) as fs, \
           ClientSession(fetch_params) as fetch, \
           ClientSession(git_params) as git:

    # Combine tools from all servers
    all_tools = []
    all_tools.extend(await fs.list_tools())
    all_tools.extend(await fetch.list_tools())
    all_tools.extend(await git.list_tools())

    # Now LLM can use tools from ALL servers!
```

---

### The Universal Pattern in One Place:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters, stdio_client

async def connect_to_mcp_server(command, args):
    """CORRECT universal MCP client template"""

    # 1. Define server parameters
    server_params = StdioServerParameters(
        command=command,
        args=args
    )

    # 2. Create stdio client (manages pipes)
    async with stdio_client(server_params) as (read, write):
        # 3. Create session with read/write streams
        async with ClientSession(read, write) as session:
            # 4. INITIALIZE FIRST! (required)
            await session.initialize()

            # 5. Now you can use all methods
            tools = await session.list_tools()
            resources = await session.list_resources()
            prompts = await session.list_prompts()

            # 6. Call tools, read resources, get prompts
            result = await session.call_tool("tool_name", {"arg": "value"})
            data = await session.read_resource("resource_uri")
            prompt = await session.get_prompt("prompt_name", {"param": "value"})

            return tools, resources, prompts, result

# Run it
async def main():
    tools, resources, prompts, result = await connect_to_mcp_server(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "."]
    )
    print(f"Found {len(tools)} tools")

asyncio.run(main())
```

---

### What You Need to Know:

| Question                                             | Answer                              |
| ---------------------------------------------------- | ----------------------------------- |
| **Do I need different client code for each server?** | **NO!** Same pattern works for all  |
| **What changes?**                                    | Just the server startup command     |
| **How do I know what tools a server has?**           | Use `list_tools()` - it tells you!  |
| **How do I know what arguments a tool needs?**       | The tool's `inputSchema` tells you  |
| **Can I use multiple servers?**                      | YES! Connect to as many as you want |

---
