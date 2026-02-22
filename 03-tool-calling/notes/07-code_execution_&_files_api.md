## Code Execution & Files API

**What it is:** Claude can run Python code in a secure Docker container and access uploaded files. This is a **server-side tool** - Claude executes the code, not you.

### Two Features Combined:

**1. Files API**

- Upload files (CSV, images, PDFs) ahead of time
- Get a `file_id` to reference later
- Files persist and can be used across conversations

**2. Code Execution Tool**

- Built-in tool (no implementation needed)
- Claude writes and runs Python code in isolated container
- No network access (secure sandbox)
- Can generate plots, analyze data, etc.

### How They Work Together:

```python
# Step 1: Upload file
file_id = upload_file("mydata.csv")

# Step 2: Use in conversation with code execution
message = {
    "role": "user",
    "content": [
        {
            "type": "container_upload",  # Special block type
            "file_id": file_id
        },
        {
            "type": "text",
            "text": "Analyze this data and show me correlations"
        }
    ]
}
```

### What Happens:

1. Claude gets file in container
2. Writes Python code to analyze it
3. Runs code, gets output
4. Can run multiple times
5. Can generate plots (saved as files)
6. Returns results + generated files

### Response Structure:

- Text blocks (analysis, explanations)
- Tool use blocks (code written)
- Code execution results (stdout, stderr)
- Generated files (available via file_id)

---

## Who Has This Feature?

| Provider             | Code Execution                        | Files API |
| -------------------- | ------------------------------------- | --------- |
| **Anthropic Claude** | ✅ YES                                | ✅ YES    |
| **OpenAI**           | ❌ No (code interpreter is different) | ❌ No     |
| **Google Gemini**    | ❌ No                                 | ❌ No     |
| **Mistral**          | ❌ No                                 | ❌ No     |
| **Llama**            | ❌ No                                 | ❌ No     |
| **DeepSeek**         | ❌ No                                 | ❌ No     |
| **OpenRouter**       | ❌ No                                 | ❌ No     |

**Note:** OpenAI has "Code Interpreter" but it works differently (runs on your end, not server-side).

---

## What You Can Learn From This

**The concept:** Some models can execute code server-side and work with uploaded files. This enables:

- Automated data analysis
- Chart generation
- Complex calculations
- File processing

**Without Claude:** You'd need to:

1. Extract code from model response
2. Run it yourself (safety concerns)
3. Handle files manually
4. Parse results back to model

**Bottom line:** Just understand the concept. It's a powerful feature but **Claude-specific**.
