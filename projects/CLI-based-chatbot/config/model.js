import "dotenv/config";

export const MODEL_CONFIG = {
  baseUrl: process.env.LOCALHOST_OLLAMA_CHAT_API,
  model: "llama3.2:1b",
  stream: false,
};
