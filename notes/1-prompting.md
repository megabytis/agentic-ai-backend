# Prompt Engineering — Core Guidelines

## Overview

Prompt engineering = giving **clear, structured instructions** to language models so they produce **reliable, relevant output**.

Two core principles:

1. **Write clear and specific instructions**
2. **Give the model time to think**

---

## Principle 1: Write Clear & Specific Instructions

### Key Idea

Clarity > brevity.  
Longer prompts are often **better** if they add context and constraints.

---

### Tactic 1: Use Delimiters

Clearly separate different parts of input.

**Examples:**

- Triple backticks `text`
- Quotes `"text"`
- XML / HTML tags `<text></text>`
- Section headers

**Why it matters:**

- Prevents confusion
- Reduces prompt injection
- Makes it obvious what text the model should act on

**Example use-case:**

> Summarize the text delimited by triple backticks into one sentence.

---

### Tactic 2: Ask for Structured Output

Request outputs in formats like:

- JSON
- HTML
- Lists

**Why it matters:**

- Easier to parse in code
- Predictable structure
- Cleaner integrations

**Example:**

```json
{
  "book_id": 1,
  "title": "...",
  "author": "...",
  "genre": "..."
}
```

---

### Tactic 3: Ask the Model to Check Conditions

Tell the model to **verify assumptions first**.

**Example logic:**

- If text contains steps → extract them
- Else → respond with `"No steps provided"`

**Why it matters:**

- Handles edge cases
- Prevents garbage outputs
- More robust pipelines

---

### Tactic 4: Few-Shot Prompting

Provide **examples before the real task**.

**Why it works:**

- Model copies tone, format, style
- Improves consistency

**Example:**
Child → Question
Grandparent → Metaphorical answer
Then ask a new question → model follows same style

---

## Principle 2: Give the Model Time to Think

### Key Idea

If reasoning is complex, **don’t let the model rush**.

Models fail the same way humans do when forced to answer fast.

---

### Tactic 1: Specify Step-by-Step Tasks

Break the task into ordered steps.

**Example structure:**

1. Summarize text
2. Translate summary
3. Extract names
4. Output JSON

**Bonus:**
Explicit output formats = easier parsing + fewer surprises.

---

### Tactic 2: Force the Model to Solve First

Tell the model to:

1. Solve the problem itself
2. THEN evaluate someone else’s solution

**Why this matters:**

- Prevents shallow agreement
- Reduces reasoning errors
- Improves correctness

**Critical line to include:**

> Do NOT decide until you have solved it yourself.

---

## Model Limitations (Very Important)

### Hallucinations

Models may:

- Invent facts
- Describe fake products
- Sound confident but be wrong

**Example:**
let's assume i'm asking a model about an non-exitence product in such a way that it feels like it does exist. Then the model will give false nd random response.

---

### How to Reduce Hallucinations

- Ask model to **find relevant information bout the provided text first**
- Then answer the question based on the relevant information.
