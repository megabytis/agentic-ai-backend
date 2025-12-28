# CLI-Based Chatbot

A modular, command-line interface (CLI) chatbot built with Node.js that demonstrates the power of **System Prompts** and **Persona Switching**. This project allows users to interact with an LLM (via Ollama) using different specialized modes.

## 🚀 Features

- **Multi-Persona Support**: Switch between different AI roles (Tutor, Coder, General Assistant) on the fly.
- **System Prompt Integration**: Demonstrates how high-level instructions shape AI behavior.
- **Conversation Memory**: Maintains context during a session.
- **Command System**: Easy-to-use slash commands for managing the chat.

## 🛠️ Commands

| Command        | Description                                         |
| -------------- | --------------------------------------------------- |
| `/mode`        | List all available AI personas/modes.               |
| `/mode <name>` | Switch to a specific persona (e.g., `/mode coder`). |
| `/current`     | Show the current active mode and its system prompt. |
| `/clear`       | Reset the conversation history.                     |
| `/bye`         | Exit the chatbot.                                   |

## 📁 Project Structure

```text
CLI-based-chatbot/
├── config/         # Model and API configurations
├── core/           # Core logic (Chat API, State management)
├── interfaces/     # CLI implementation
├── prompts/        # System prompt definitions (Modes)
└── index.js        # Entry point
```

## ⚙️ Prerequisites

- **Node.js**: v18 or higher.
- **Ollama**: Running locally with the `gemma:2b` model (or update `config/model.js` to your preferred model).

## 🏃 How to Run

1. Ensure Ollama is running:

   ```bash
   ollama run gemma:2b
   ```

2. Navigate to the project directory:

   ```bash
   cd projects/CLI-based-chatbot
   ```

3. Start the chatbot:
   ```bash
   node index.js
   ```

## 💡 Key Concept: System Prompts

This project highlights the use of **System Prompts**. Unlike user messages, system prompts are high-level instructions provided to the model to define its:

- **Persona**: Who is the AI? (e.g., "You are a math tutor").
- **Constraints**: What should it NOT do? (e.g., "Do not give direct answers").
- **Tone**: How should it speak? (e.g., "Be concise and professional").
