# MCP Architecture Fundamentals

### Q1. Can you explain, in your own words, what an MCP client is and what it's primary role is in the MCP architecture?

- MCP client is the communication bridge between our server and MCP server. what it does actually, it takes our request and give it to MCP server and vice-versa. It handles all messages like ListToolRequest, ListToolResponse, CallToolRequest, CallToolResponse

### Q2. To elaborate a bit more, what kind of requests does an MCP client typically send to an MCP server, and what is the ultimate goal of these interactions?

- Translates your server's requests into MCP spec messages
- Manages connection to MCP server(s)
- Handles multiple servers simultaneously

# Implementing MCP Servers

### Q3. When you're defining tools in an MCP server, what is the main benefit of using decorators with the Python SDK?

- The main benefit of using decorators (such as @mcp.tool(), @server.tool(), or equivalent in the MCP Python SDK/FastMCP) when defining tools in an MCP server is simplicity and declarative registration.
- Decorators allow us to turn a plain Python function into a fully exposed MCP tool with minimal boilerplate. We write a regular function with type hints and a docstring (which the SDK uses to auto-generate the tool schema, parameters, and description that the AI/LLM client sees), then apply the decorator.

Example:

```py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool()  # This is the decorator
def add(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b
```

# Client-Server Interaction

### Q4. Once you have your MCP server set up with its tools, how does a client typically establish a connection with the server, and what's an important aspect of ensuring that communication is successful?

- first of all our server will send let's suppose 'ListToolRequest' to MCP client, then MCP client will pass that Req to MCP server, then MCP server will give 'ListToolsResult' as response to MCP client , then client serve it to our server

### Q5. Before any of these requests can be sent, the client first needs to connect to the MCP server. What's the initial step a client takes to establish that connection, and what might be a common way to ensure the server is ready to receive these connections?

- Client first connects to the MCP server (via WebSocket, SSE, or stdio).
- Then sends an **initialize** request (JSON-RPC).
- Server starts listening on the port & replies, client sends **initialized** notification.
- After that, client can send 'ListToolsRequest' to discover available tools.
- Server must be running and listening on the port before client connects.

# Debugging with the MCP Inspector

### Q6. Imagine you've set up your MCP server and client, but you suspect there's an issue with how one of your tools is behaving. How can the MCP Inspector help you diagnose and fix this problem?

- MCP Inspector is a web-based tool for testing MCP servers. Connect to your running server, go to Tools tab, select the problematic tool, input custom arguments, and call it. View execution results, raw JSON, schemas, and real-time logs/notifications to spot issues and fix behavior.
