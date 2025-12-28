import { MODES } from "../prompts/modes.js";

export const state = {
  messages: [],
  currentMode: "general",
};

export const addUserMessage = (text) => {
  state.messages.push({ role: "user", content: text });
};

export const addAssistantMessage = (text) => {
  state.messages.push({ role: "assistant", content: text });
};

export const clearConversation = () => {
  state.messages.length = 0;
};

export const changeMode = (mode) => {
  state.currentMode = mode;
  clearConversation();
};

export const getSystemPrompt = () => {
  return MODES[state.currentMode];
};
