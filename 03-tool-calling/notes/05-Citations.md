## Citations

**What is it?**
A Claude-specific feature that allows the model to **cite exact sources** (PDFs, text) when answering questions. It returns structured data showing exactly where information came from.

**How it works:**

- When you provide a document (PDF or text) with `citations: {"enabled": true}`
- Claude's response includes citation objects with:
  - **Cited text** - The actual source text used
  - **Document title/index** - Which document it came from
  - **Page numbers** - For PDFs (start/end page)
  - **Character positions** - For plain text (start/end char)

**Example response structure:**

```json
{
  "citations": [
    {
      "cited_text": "Earth's atmosphere was formed by volcanic outgassing...",
      "document_title": "earth.pdf",
      "start_page": 4,
      "end_page": 5
    }
  ]
}
```

**Why it's useful:**

- **Transparency** - Users see exactly where information comes from
- **Verification** - Can check if Claude interpreted correctly
- **UI features** - Build hover pop-ups, footnotes, source panels

---

## Who Has This Feature?

| Provider                   | Citations Support           |
| -------------------------- | --------------------------- |
| **Anthropic Claude**       | ✅ **YES** - Native feature |
| **OpenAI** (GPT-4, etc.)   | ❌ No                       |
| **Google Gemini**          | ❌ No                       |
| **Mistral**                | ❌ No                       |
| **Llama** (any version)    | ❌ No                       |
| **DeepSeek**               | ❌ No                       |
| **Qwen**                   | ❌ No                       |
| **OpenRouter** (any model) | ❌ No                       |

**Currently, ONLY Claude has this built-in citation feature.**

---

## What Others Have Instead

| Provider       | Alternative                                                     |
| -------------- | --------------------------------------------------------------- |
| **OpenAI**     | Function calling (you'd need to build citation system yourself) |
| **Gemini**     | Grounding with Google Search (web citations only)               |
| **Perplexity** | Built-in web citations in their UI (not API)                    |
| **You.com**    | Web citations in their UI                                       |

**Bottom line:** Citations is a **Claude-exclusive feature** - you'd need to build your own system to replicate it with other models.
