Here are the **universal parameters** used in 95% of GenAI applications, regardless of the provider or setup:

## 🎯 **CORE PARAMETERS (Use Everywhere)**

### 1. **`model`** (Required)

```javascript
// Every single API call needs this
{ model: "gpt-4", model: "claude-3", model: "llama3.2:1b" }
```

**Why:** Specifies which AI model to use. Different models = different capabilities/prices.

### 2. **`messages` / `prompt`** (Required)

```javascript
// Two main formats:
// Format A: Chat format (OpenAI, Anthropic, etc.)
messages: [
  { role: "system", content: "You are a helpful assistant" },
  { role: "user", content: "Hello!" },
];

// Format B: Simple prompt (Ollama, some local models)
prompt: "Hello, how are you?";
```

**Why:** The input text that the model responds to.

### 3. **`temperature`** (0.0 to 1.0 or 2.0)

```javascript
temperature: 0.7; // Most common default
// 0.0 = Deterministic, repetitive
// 0.7 = Balanced creativity
// 1.0+ = Very creative, random
```

**Why:** Controls randomness. **Use 0.7 for most tasks, 0.2 for code/facts, 0.9 for creative writing.**

### 4. **`max_tokens` / `max_length`**

```javascript
max_tokens: 1000; // Limits response length
```

**Why:** Prevents infinite responses and controls costs. **Always set this!**

## 🔧 **ESSENTIAL PARAMETERS (Use Often)**

### 5. **`stream`**

```javascript
stream: true; // For real-time responses
stream: false; // For complete response at once (default)
```

**Why:** User experience. **Always use `stream: true` for chat UIs.**

### 6. **`top_p`** (Alternative to temperature)

```javascript
top_p: 0.9; // Most common
// Use EITHER temperature OR top_p, not both
```

**Why:** Nucleus sampling - often gives better results than temperature alone.

### 7. **`stop`** / **`stop_sequences`**

```javascript
stop: ["\n", "Human:", "AI:"]; // Stop generation when these appear
```

**Why:** Controls where the response ends. Crucial for structured outputs.

### 8. **`frequency_penalty` & `presence_penalty`** (OpenAI-specific but useful concepts)

```javascript
frequency_penalty: 0.0; // -2.0 to 2.0
presence_penalty: 0.0; // -2.0 to 2.0
```

**Why:** Controls repetition. Positive = avoid repetition, Negative = allow repetition.

## 📊 **PRODUCTION PARAMETERS (For serious apps)**

### 9. **`seed`** (For reproducible outputs)

```javascript
seed: 42; // Any integer
```

**Why:** Makes outputs reproducible. Critical for testing/debugging.

### 10. **`response_format`** (For structured output)

```javascript
// OpenAI-style
response_format: { type: "json_object" }

// Or with tools/function calling
tools: [...]
tool_choice: "auto"
```

**Why:** Forces JSON output or enables function calling.

### 11. **`n`** (Number of completions)

```javascript
n: 1; // How many different responses to generate
```

**Why:** Generate multiple alternatives (costs more).

## 💡 **THE 5-PARAMETER UNIVERSAL TEMPLATE**

For 80% of your work, just use these 5:

```javascript
const completion = await client.chat.completions.create({
  model: "gpt-4", // 1. Which model
  messages: [
    // 2. The conversation
    { role: "user", content: "Hello" },
  ],
  temperature: 0.7, // 3. Creativity control
  max_tokens: 1000, // 4. Length limit
  stream: false, // 5. Streaming on/off
});
```

## 🚀 **PRO TIPS - These Never Change:**

1. **Temperature:** `0.7` for chat, `0.2` for code/facts, `0.9` for creative
2. **Always set `max_tokens`:** Never trust unlimited responses
3. **Use streaming in production:** Better UX
4. **System prompt matters:** 70% of output quality comes from good system prompt
5. **Seed for consistency:** Use `seed` when testing

## 🔄 **Parameter Mapping Across Providers:**

| **Concept** | **OpenAI**          | **Anthropic** | **Ollama**          | **Gemini**          |
| ----------- | ------------------- | ------------- | ------------------- | ------------------- |
| Model       | `model`             | `model`       | `model`             | `model`             |
| Input       | `messages`          | `messages`    | `messages`/`prompt` | `contents`          |
| Creativity  | `temperature`       | `temperature` | `temperature`       | `temperature`       |
| Length      | `max_tokens`        | `max_tokens`  | `num_predict`       | `max_output_tokens` |
| Streaming   | `stream`            | `stream`      | `stream`            | `stream`            |
| Repetition  | `frequency_penalty` | -             | `repeat_penalty`    | -                   |

## 🎓 **Our GenAI Career Stack:**

**Learn these 7 parameters thoroughly:**

1. `model` - Which brain
2. `messages`/`prompt` - What to say
3. `temperature` - How creative
4. `max_tokens` - How long
5. `stream` - How to deliver
6. `stop` - When to stop
7. `seed` - For consistency
