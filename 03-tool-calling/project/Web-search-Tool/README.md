# Web Search Tool - AI-Powered Chatbot with Real-Time Search

A Python-based chatbot that combines OpenAI/OpenRouter LLMs with real-time web search capabilities using DuckDuckGo. Features domain restriction, tool calling, and streaming responses.

## Features

- 🌐 **Real-time Web Search**: Integrates DuckDuckGo search for current information
- 🔍 **Domain Restriction**: Limit searches to specific domains (e.g., `nih.gov`, `reuters.com`)
- 🛠️ **Multi-Tool Support**:
  - Web search
  - Date/time functions
  - Reminder setting
  - Batch tool execution
- ⚡ **Streaming Responses**: Real-time token-by-token output
- 💭 **Thinking Mode**: Optional step-by-step reasoning (prompt-based)
- 🔄 **Conversation History**: Maintains context across interactions

## Prerequisites

- Python 3.8+
- OpenRouter API key (free tier available)
- Required packages: `openai`, `python-dotenv`, `ddgs`

## Installation

```bash
# Clone repository
git clone <your-repo-url>
cd web-search-tool

# Install dependencies
pip install openai python-dotenv ddgs

# Create .env file with your API key
echo "OPENROUTER_API_KEY=your-key-here" > .env
```

## Usage

```bash
python main.py
```

### Commands:

- `/bye` - Exit chatbot
- `/think` - Toggle thinking mode (prompt-based reasoning)

### Example Queries:

```bash
# Basic search
You: What happened in AI news this week?

# Domain-restricted search
You: Find medical research from nih.gov about exercise

# Multi-step with tools
You: What's today's date? Search for news from this week.

# Complex reasoning with thinking mode
You: /think
You: If a train leaves at 3pm going 60mph and another at 4pm going 70mph, when will they meet?
```

## Tool Schemas

### Web Search Tool

```python
{
    "name": "web_search",
    "description": "Search the web for current information",
    "parameters": {
        "query": "search query",
        "max_results": 10,  # optional
        "allowed_domains": ["example.com"]  # optional
    }
}
```

### Supported Tools

- `get_current_time` - Current time in HH:MM:SS
- `get_current_date` - Current date in YYYY-MM-DD
- `get_current_datetime` - Combined date and time
- `add_duration_to_datetime` - Add days/weeks/hours to a date
- `set_reminder` - Set a reminder message
- `run_batch` - Execute multiple tools in one call
- `web_search` - Search the web

## Configuration

Edit `main.py` to change:

- `MODEL` - OpenRouter model (default: `stepfun/step-3.5-flash:free`)
- `MAX_ITERATIONS` - Maximum tool call rounds (default: 5)
- System prompt - Modify assistant behavior

## Project Structure

```
web-search-tool/
├── main.py              # Main chatbot implementation
├── .env                 # API keys (not in repo)
├── README.md            # This file
└── requirements.txt     # Dependencies
```

## Dependencies

```
openai>=1.0.0
python-dotenv>=1.0.0
duckduckgo-search>=6.0.0
```

## How It Works

1. User input → Added to message history
2. LLM decides to call web_search tool or respond directly
3. If search needed:
   - DuckDuckGo searches with optional domain filtering
   - Results formatted and returned to LLM
4. LLM generates final response with citations
5. All interactions streamed in real-time

## Limitations

- Free OpenRouter models have rate limits
- DuckDuckGo may block excessive automated queries
- Domain filtering is client-side (after search)
- Thinking mode is prompt-based, not native model reasoning

## Future Improvements

- [ ] Add caching for repeated searches
- [ ] Implement search result summarization
- [ ] Add more search providers (Tavily, SerpAPI)
- [ ] Improve citation formatting
- [ ] Add conversation memory persistence

## License

MIT License - Feel free to use and modify!

## Acknowledgments

- OpenRouter for free LLM access
- DuckDuckGo for search API
- Anthropic for tool-calling inspiration
