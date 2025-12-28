import { MODEL_CONFIG } from "../config/model.js";

export const chat = async ({ messages, systemPrompt }) => {
  try {
    // // Debugging : what system prompt is
    // console.log(`\n> Sending system prompt (mode: ${currentMode}):`);
    // console.log(
    //   `> "${system?.substring(0, 100)}${system?.length > 100 ? "..." : ""}"\n`
    // );

    const response = await fetch(MODEL_CONFIG.baseUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: MODEL_CONFIG.model,
        messages,
        system: systemPrompt,
        stream: MODEL_CONFIG.stream,
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
