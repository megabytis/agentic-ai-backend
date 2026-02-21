## Prompt Caching - Brief Note

**What it is:** A feature that caches the computational work done on input messages so repeated requests with the same prefix are faster and cheaper.

**How it works:**

1. First request: Claude processes input, creates internal representations
2. These representations are **cached** instead of discarded
3. Subsequent requests with the **same prefix** reuse the cached work
4. Results: **Faster responses, lower cost** (up to 90% cost reduction)

**When to use it:**

- Long system prompts used repeatedly
- Large documents analyzed multiple times
- Multi-turn conversations with long history
- Tools/instructions that don't change between requests

---

## Who Has Prompt Caching?

| Provider             | Prompt Caching Support                                  |
| -------------------- | ------------------------------------------------------- |
| **Anthropic Claude** | ✅ **YES** - Native feature with `cache_control`        |
| **OpenAI**           | ✅ **YES** (recently added) - Available for some models |
| **Google Gemini**    | ❌ Not directly (context caching is different)          |
| **Mistral**          | ❌ No                                                   |
| **Llama**            | ❌ No                                                   |
| **DeepSeek**         | ❌ No                                                   |
| **Qwen**             | ❌ No                                                   |
| **OpenRouter**       | ⚠️ Depends on underlying model                          |

---

## Implementation (if your model supports it)

**Claude-style implementation:**

```python
messages = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are a helpful assistant...",
                "cache_control": {"type": "ephemeral"}  # <-- Cache this
            }
        ]
    },
    {
        "role": "user",
        "content": "Actual user query here"
    }
]
```

**OpenAI implementation (if available):**

```python
# Check OpenAI docs for current cache implementation
# Usually automatic for repeated prefixes
```

---

## What You Can Do Without Built-in Caching

**Option 1: Manual Caching (Client-side)**

```python
# Cache long system prompts locally
cached_system_prompt = "Your very long system prompt here..."

# Just reuse it - saves token count but not compute
messages = [
    {"role": "system", "content": cached_system_prompt},
    {"role": "user", "content": user_input}
]
```

**Option 2: Session-based Reuse**

```python
# For multi-turn conversations, reuse the same messages list
# This is what your code already does!
messages.append(user_message)
messages.append(assistant_response)
```

**Option 3: Embedding-based Retrieval**

```python
# For RAG-style systems
# Store document chunks in vector DB, retrieve relevant ones
# This is different from prompt caching but achieves similar goals
```

---

## Bottom Line

**Prompt caching is a server-side optimization** - you can't truly implement it yourself. It depends on the API provider supporting it.

**Your existing code already does client-side "caching"** by reusing the `messages` list across turns. This saves tokens but not compute.

**Check your specific model's docs** to see if prompt caching is supported on OpenRouter for that model.
