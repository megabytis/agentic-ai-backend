import readline from "readline";
import dotenv from "dotenv";
dotenv.config();

const messages = [
  {
    role: "system",
    content: "```json",
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
    const response = await fetch(process.env.LOCALHOST_OLLAMA_CHAT_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "llama3.2:3b",
        messages,
        stream: false,
        // options: {
        //   temperature: 0.7,
        //   stop: ["```"],
        // },
        format: "json",
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
      console.log("\n🤖Assistant: ", reply, "\n");
      addAssistantMessage(reply);
    } catch (err) {
      console.log("Error: ", err.message);
    }

    promptUser();
  });
};

promptUser();
