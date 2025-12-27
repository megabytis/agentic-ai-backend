const add_user_message = (messages, text) => {
  const user_message = { role: "user", content: text };
  messages.push(user_message);
};

const add_assistant_message = (messages, text) => {
  const assistant_message = { role: "assistant", content: text };
  messages.push(assistant_message);
};

const chat = async (messages) => {
  try {
    const response = await fetch("http://localhost:11434/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "gemma:2b", //"gemini-3-flash-preview:cloud",
        messages: messages,
        stream: false,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const jsonData = await response.json();
    return jsonData.message.content;
  } catch (error) {
    console.error("Chat error:", error);
    throw error;
  }
};

const messages = [];
messages.push({
  role: "system",
  content:
    "You are a helpful assistant that explains GenAI concepts clearly and concisely.",
});

const userPrompt = async (text) => {
  add_user_message(messages, text);
  const response = await chat(messages);
  console.log("👨User: ", text);
  console.log("🤖Assistant:", response, "\n");
  add_assistant_message(messages, response);
};

await userPrompt("Hello");
await userPrompt("I just started learning GenAI");
await userPrompt("tell me something about it ");
await userPrompt("How is it different from ML?");
