import readline from "readline";
import {
  state,
  addUserMessage,
  addAssistantMessage,
  clearConversation,
  changeMode,
  getSystemPrompt,
} from "../core/state.js";
import { chat } from "../core/chat.js";
import { MODES } from "../prompts/modes.js";

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

console.log("CLI chatbot started. Type '/bye' to quit.\n");

const promptUser = () => {
  rl.question(`👨You [${state.currentMode}]: `, async (input) => {
    const cmd = input.toLowerCase();

    // QUIT
    if (cmd === "/bye") {
      rl.close();
      return;
    }

    // MODE without arguments: to show available modes
    if (cmd === "/mode") {
      console.log("\nAvailable modes:");
      Object.keys(MODES).forEach((m) => console.log("- ", m));
      console.log("\nUse: /mode <mode_name>\n");

      return promptUser();
    }

    // MODE with arguments: to actually change mode
    if (cmd.startsWith("/mode ")) {
      const newMode = input.split(" ")[1].toLowerCase();
      if (MODES[newMode]) {
        changeMode(newMode); // reseting memory after changing mode
        console.log(`\nMode changed to: ${newMode}\n`);
      } else {
        console.log(`\nUnknown mode: ${newMode}`);
        console.log("Available modes:", Object.keys(MODES).join(", "), "\n");
      }

      return promptUser();
    }

    // To show current mode without switching
    if (cmd === "/current") {
      console.log(`\nCurrent mode: ${state.currentMode}`);
      console.log(`Prompt: ${getSystemPrompt()}\n`);

      return promptUser();
    }

    // To RESET conversation
    if (cmd === "/clear") {
      clearConversation();
      console.log("\nConversation cleared!\n");
      return promptUser();
    }

    // MODEL CALL
    try {
      addUserMessage(input);
      const reply = await chat({
        messages: state.messages,
        systemPrompt: getSystemPrompt(),
      });

      console.log("\n🤖Assistant: ", reply, "\n");
      addAssistantMessage(reply);
    } catch (err) {
      console.log("Error: ", err.message);
    }

    promptUser();
  });
};

promptUser();
