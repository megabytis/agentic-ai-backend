import readline from "readline";
import { chat } from "../model.js";

export const messages = [];

const addUserMessage = (text) => {
  const userMessage = { role: "user", content: text };
  messages.push(userMessage);
};

const addAssistantMessage = (text) => {
  const assistantMessage = { role: "assistant", content: text };
  messages.push(assistantMessage);
};

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

console.log("CLI chatbot started. Type '/bye' to quit.\n");

// Chat-Modes
const modes = {
  tutor:
    "You are a patient math tutor. Do not directly answer a student's questions. Guide them to a solution step by step.",
  coder:
    "You are an expert programming assistant. Explain code concepts clearly with examples.",
  general: "You are a helpful, harmless, and honest assistant.",
};
export let currentMode = "tutor";

const promptUser = () => {
  rl.question(`👨You [${currentMode}]: `, async (input) => {
    // QUIT
    if (input.toLowerCase() === "/bye") {
      rl.close();
      return;
    }

    // MODE without arguments: to show available modes
    if (input.toLocaleLowerCase() === "/mode") {
      let counter = 1;
      console.log("\nAvailable modes:");
      for (const mode of Object.keys(modes)) {
        console.log(`${counter}. ${mode}`);
        counter++;
      }
      console.log("\nSpecify mode with format: '/mode <mode_name>'\n");
      promptUser();
      return;
    }

    // MODE with arguments: to actually change mode
    if (input.toLowerCase().startsWith("/mode ")) {
      const newMode = input.split(" ")[1].toLowerCase();
      if (modes[newMode]) {
        currentMode = newMode;
        messages.length = 0; // reseting memory after changing mode
        console.log(`\nMode changed to: ${newMode}\n`);
      } else {
        console.log(`\nUnknown mode: ${newMode}`);
        console.log("Available modes:", Object.keys(modes).join(", "), "\n");
      }
      promptUser();
      return;
    }

    // To show current mode without switching
    if (input.toLowerCase() === "/current") {
      console.log(`\nCurrent mode: ${currentMode}`);
      console.log(`Prompt: ${modes[currentMode]}\n`);
      promptUser();
      return;
    }

    // To RESET conversation
    if (input.toLowerCase() === "/clear") {
      messages.length = 0;
      console.log("\nConversation cleared!\n");
      promptUser();
      return;
    }

    // MODEL CALL
    try {
      addUserMessage(input);
      const reply = await chat(modes[currentMode]);
      console.log("\n🤖Assistant: ", reply, "\n");
      addAssistantMessage(reply);
    } catch (err) {
      console.log("Error: ", err.message);
    }

    promptUser();
  });
};

console.log(`Current mode: ${currentMode}\n`);
promptUser();
