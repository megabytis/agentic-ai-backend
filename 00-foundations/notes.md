## What is GenAI (engineering view)

- GenAI = probabilistic function approximator over tokens
- LLMs do NOT “remember” — context must be resent
- Output quality = f(model, prompt, context, temperature)

## Core primitives

- Prompt: instruction + constraints
- Context window: hard limit, cost driver
- Tokens: billing + truncation risk
- Temperature: randomness vs determinism

## Mental model

User Input
→ Prompt Construction
→ Model Inference
→ Output Parsing
→ (Optional) Tool Calls
→ Final Response

## What I am NOT learning here

- Model training math
- Gradient descent
- Transformer internals (deep math)

## What I AM learning

- How to CONTROL models
- How to STRUCTURE context
- How to DESIGN systems around LLMs
