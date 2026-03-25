## MCP Clients

**What is an MCP Client?**
The **communication bridge** between your application and MCP servers. It handles all the messaging defined in the MCP spec.

### The 4 Core Message Types:

| Message              | Direction       | Purpose                                  |
| -------------------- | --------------- | ---------------------------------------- |
| **ListToolsRequest** | Client → Server | "What tools do you have?"                |
| **ListToolsResult**  | Server → Client | "Here are my tools: [tool1, tool2, ...]" |
| **CallToolRequest**  | Client → Server | "Run tool X with these arguments"        |
| **CallToolResult**   | Server → Client | "Here's the result: [data]"              |

### Complete MCP Flow (Step by Step):

```
┌──────┐     ┌──────────┐     ┌─────────┐     ┌─────────┐     ┌────────┐     ┌───────┐
│ User │     │  Your    │     │   MCP   │     │   MCP   │     │External│     │ Claude│
│      │     │  Server  │     │ Client  │     │ Server  │     │Service │     │       │
└──┬───┘     └────┬─────┘     └─────┬───┘     └────┬────┘     └───┬────┘     └───┬───┘
   │              │                 │              │              │              │
   │ 1. Query     │                 │              │              │              │
   │─────────────>│                 │              │              │              │
   │              │                 │              │              │              │
   │              │ 2. ListToolsReq │              │              │              │
   │              │────────────────>│              │              │              │
   │              │                 │ 3. ListToolsReq             │              │
   │              │                 │─────────────>│              │              │
   │              │                 │              │              │              │
   │              │                 │ 4. ListToolsResult          │              │
   │              │                 │<─────────────│              │              │
   │              │ 5. ListToolsResult             │              │              │
   │              │<────────────────│              │              │              │
   │              │                 │              │              │              │
   │              │ 6. Query + Tools│              │              │              │
   │              │─────────────────────────────────────────────────────────────>│
   │              │                 │              │              │              │
   │              │                 │              │ 7. Tool Use Response        │
   │              │<─────────────────────────────────────────────────────────────│
   │              │                 │              │              │              │
   │              │ 8. CallToolReq  │              │              │              │
   │              │────────────────>│              │              │              │
   │              │                 │ 9. CallToolReq              │              │
   │              │                 │─────────────>│              │              │
   │              │                 │              │ 10. API Call │              │
   │              │                 │              │─────────────>│              │
   │              │                 │              │              │              │
   │              │                 │              │ 11. API Response            │
   │              │                 │              │<─────────────│              │
   │              │                 │ 12. CallToolResult          │              │
   │              │                 │<─────────────│              │              │
   │              │ 13. CallToolResult             │              │              │
   │              │<────────────────│              │              │              │
   │              │                 │              │              │              │
   │              │ 14. Tool Result───────────────>│              │              │
   │              │─────────────────────────────────────────────────────────────>│
   │              │                 │              │              │              │
   │              │ 15. Final Response             │              │              │
   │              │<─────────────────────────────────────────────────────────────│
   │              │                 │              │              │              │
   │ 16. Answer   │                 │              │              │              │
   │<─────────────│                 │              │              │              │
   └──────────────┴─────────────────┴──────────────┴──────────────┴──────────────┘
```

```
| Step   | What Happens                                             | In Our Example                                                      |
| ------ | -------------------------------------------------------- | ------------------------------------------------------------------- |
| **1**  | User sends a query                                       | You type: *"What's the weather in Paris?"*                          |
| **2**  | Your Server asks MCP Client: *"What tools do you have?"* | "Hey, what tools are available?"                                    |
| **3**  | MCP Client forwards to MCP Server                        | Passes the question along                                           |
| **4**  | MCP Server replies: *"I have a `get_weather` tool"*      | Lists available tools                                               |
| **5**  | Your Server receives the tool list                       | Now knows about `get_weather`                                       |
| **6**  | Your Server sends query + tools to Claude                | "Here's what the user asked, and here's a weather tool you can use" |
| **7**  | Claude decides to use the tool                           | Claude: *"I should use `get_weather` for Paris"*                    |
| **8**  | Your Server tells MCP Client: *"Call the weather tool"*  | Execute the tool                                                    |
| **9**  | MCP Client forwards to MCP Server                        | Passes the execution request                                        |
| **10** | MCP Server calls the actual Weather API                  | Fetches real weather data from weather.com (or similar)             |
| **11** | Weather API returns data                                 | *"72°F, sunny"*                                                     |
| **12** | MCP Server returns result to Client                      | Passes weather data back                                            |
| **13** | MCP Client returns result to Your Server                 | Your server now has the weather                                     |
| **14** | Your Server sends tool result to Claude                  | "Here's the weather data"                                           |
| **15** | Claude generates final response                          | *"It's 72°F and sunny in Paris!"*                                   |
| **16** | Your Server shows answer to you                          | You see the friendly response                                       |

```

### Key Points:

1. **Transport Agnostic** - MCP can communicate over:
   - **STDIO** (same machine) - most common for local development
   - **HTTP/WebSockets** - for remote servers
   - Any other protocol that can exchange messages

2. **Your Server's Role**:
   - No longer executes tools directly
   - Just orchestrates between Claude and MCP client

3. **MCP Client's Role**:
   - Translates your server's requests into MCP spec messages
   - Manages connection to MCP server(s)
   - Handles multiple servers simultaneously

### Why This Architecture?

| Without MCP                              | With MCP                        |
| ---------------------------------------- | ------------------------------- |
| Your server has ALL tool implementations | Your server just orchestrates   |
| You write EVERY tool                     | Tools come from MCP servers     |
| Hard to add new services                 | Plug in new MCP servers easily  |
| Tight coupling to APIs                   | Loose coupling via MCP protocol |

**Bottom line:** The MCP client is your app's connection point to the MCP ecosystem. It handles all the protocol messaging so you don't have to!
