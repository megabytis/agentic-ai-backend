## Simple MCP Learning Project - Free & Practical

**Project:** A **Weather Info Bot** that uses MCP to separate weather data fetching from the main chatbot.

---

### Project Architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR PROJECT                             │
│                      (mcp-weather/)                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐         ┌─────────────────────────┐    │
│  │   MCP Client    │◄───────►│    Weather MCP Server   │    │
│  │  (client.py)    │  STDIO  │                         │    │
│  └─────────────────┘         │ • get_weather tool      │    │
│         │                    │ • get_forecast tool     │    │
│         │                    └─────────────────────────┘    │
│         │                               │                   │
│         │                               ▼                   │
│  ┌──────▼──────┐              ┌─────────────────────────┐   │
│  │  OpenRouter │              │   Free Weather API      │   │
│  │    (free)   │              │   (wttr.in - no key)    │   │
│  └─────────────┘              └─────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Project Structure:

```
mcp-weather/
├── client.py              # Main chatbot + MCP client
├── weather_server.py      # MCP server with weather tools
├── .env                   # OpenRouter API key only
├── requirements.txt       # Dependencies
└── README.md              # Your notes
```

---

### Step 1: Setup Files

**requirements.txt:**

```
openai>=1.0.0
python-dotenv>=1.0.0
requests>=2.28.0
mcp>=0.1.0  # If available, otherwise we'll implement simple version
```

**.env:**

```
OPENROUTER_API_KEY=your-key-here
```

---

### Step 3: Run It!

```bash
# 1. Install dependencies
pip install openai python-dotenv requests

# 2. Add your OpenRouter key to .env
echo "OPENROUTER_API_KEY=your-key-here" > .env

# 3. Run the chatbot
python client.py
```

---

### What You'll See:

```
✅ Loaded 2 tools from MCP server

🌤️  Weather Bot with MCP
Type 'quit' to exit

You: What's the weather in London?

Bot:
🔧 Calling tool: get_weather
📦 Result: {'city': 'London', 'weather': 'Light rain +12°C', 'source': 'wttr.in (free)'}

The weather in London is currently light rain with a temperature of 12°C.
```

---

### How This Demonstrates MCP:

| Concept            | In This Project                                              |
| ------------------ | ------------------------------------------------------------ |
| **MCP Server**     | `weather_server.py` - knows weather APIs, exposes tools      |
| **MCP Client**     | `SimpleMCPClient` in `client.py` - talks to server via STDIO |
| **Tool Discovery** | Client asks server for tools with `list_tools`               |
| **Tool Execution** | Client sends `call_tool` to server, server calls weather API |
| **Separation**     | Main app doesn't know weather logic - just uses MCP          |
