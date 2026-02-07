# AI Chatbot with Tool Calling

## 🎯 Features
- **5 integrated tools**: Time/date functions with calculations
- **Tool chaining**: One tool's output feeds into another
- **Multi-provider support**: OpenRouter, Ollama, Groq
- **Error handling**: Graceful tool execution failures
- **Interactive CLI**: Real-time conversation

## 🛠️ Tools Available
1. `get_current_time()` - Current time in HH:MM:SS
2. `get_current_date()` - Current date in YYYY-MM-DD  
3. `get_current_datetime()` - Full datetime
4. `add_duration_to_datetime()` - Date/time calculations
5. `set_reminder()` - Schedule reminders

## 🚀 Usage Examples

User: "Set a reminder for 10 days after today about my exam"
AI: [Calls get_current_datetime → add_duration_to_datetime → set_reminder]
Output: "Reminder set for 2026-02-17 22:17:02: UPSC exam"


## 📊 Performance
- **GPT-OSS-120b**: Excellent tool calling (production quality)
- **Local models (7B+)**: Good with proper prompting
- **Small models (<3B)**: Limited tool calling ability

## 🎓 Learning Outcomes
- Tool schema definition (OpenAI format)
- Multi-tool orchestration
- Error handling in AI workflows
- Provider abstraction layer
