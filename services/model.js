import { currentMode, messages } from "./1-prompting/4-system-prompt.js";

export const chat = async (system = null) => {
  try {
    // Debugging : what system prompt is
    console.log(`\n> Sending system prompt (mode: ${currentMode}):`);
    console.log(
      `> "${system?.substring(0, 100)}${system?.length > 100 ? "..." : ""}"\n`
    );

    const response = await fetch("http://localhost:11434/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "gemma:2b", //"gemini-3-flash-preview:cloud",
        messages,
        stream: false,
        system: system,
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
