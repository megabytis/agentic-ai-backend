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

## Rules of Prompt Caching

### 1. **Cache Breakpoints**

- Add `cache_control: {"type": "ephemeral"}` to any block
- Everything **before and including** that block gets cached
- Must use **long-form** syntax (not the shorthand string)

### 2. **Cache Duration**

- Cache lasts for **1 hour** only
- After that, it's gone and you pay full price again

### 3. **Order Matters**

Content is joined in this order:

1. **Tools** (if any)
2. **System prompt**
3. **Messages**

Where you place breakpoints determines what gets cached.

### 4. **Multiple Breakpoints**

- Can have up to **4 breakpoints** per request
- Each breakpoint creates a separate cacheable segment
- If earlier content changes, later caches remain valid

### 5. **Minimum Size**

- Must cache at least **1024 tokens**
- Tiny blocks won't be cached (e.g., just "hi there")

### 6. **What Can Be Cached**

- ✅ Text blocks
- ✅ Image blocks
- ✅ Tool use/results
- ✅ Tool schemas
- ✅ System prompts

### 7. **Cache Invalidation**

Cache breaks if ANY content **before a breakpoint** changes:

- Even one word difference = cache miss
- Content after breakpoint can change freely

---

## Summary Cheat Sheet

| Rule                | Detail                                 |
| ------------------- | -------------------------------------- |
| **Syntax**          | `cache_control: {"type": "ephemeral"}` |
| **Duration**        | 1 hour                                 |
| **Max breakpoints** | 4 per request                          |
| **Min tokens**      | 1024                                   |
| **Order**           | Tools → System → Messages              |
| **Invalidation**    | Any change before breakpoint           |

**Bottom line:** Just understand these rules. You'll use them if you ever work with Claude or another provider that supports prompt caching.
