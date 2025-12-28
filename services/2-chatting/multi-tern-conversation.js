import readline from "readline";

const messages = [
  {
    role: "system",
    // content:
    // "You are a helpful assistant that explains GenAI concepts clearly and concisely.",
  },
];

const addUserMessage = (text) => {
  const userMessage = { role: "user", content: text };
  messages.push(userMessage);
};

const addAssistantMessage = (text) => {
  const assistantMessage = { role: "assistant", content: text };
  messages.push(assistantMessage);
};

const chat = async () => {
  try {
    const response = await fetch("http://localhost:11434/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "gemma:2b", //"gemini-3-flash-preview:cloud",
        messages,
        stream: false,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.message.content;
  } catch (error) {
    console.error("Chat error:", error);
    throw error;
  }
};

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

console.log("CLI chatbot started. Type 'exit' to quit.\n");

const promptUser = () => {
  rl.question("You: ", async (input) => {
    if (input.toLowerCase() === "exit") {
      rl.close();
      return;
    }

    try {
      addUserMessage(input);
      const reply = await chat();
      console.log("🤖Assistant: ", reply, "\n");
      addAssistantMessage(reply);
    } catch (err) {
      console.log("Error: ", err.message);
    }

    promptUser();
  });
};

promptUser();
