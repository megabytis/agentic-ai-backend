## What Token is ?

- Tokens are like subwords / smallest parts of a text
- e.g. in "Hey there!", there r 3 tokens nd they are "Hey", " there" & "!"
- tokens matter bcuz they charge per token, number of token usage increase, cost will increase

## Why context window matters

- for e.g. google gemini context window is 1M i.e. means our total input + output should remain within 1M otherwise it would be more expensive
- and 1M context window is very huge so that an entire book can fit

## Why the model is stateless

- stateless means the model has no memory i.e. what we chat with it earlier it never remembers.

## What the model actually does when you call it

- when we call a model e.g. i send "hi"
- it will first convert the "hi" into tokens & will predict the next token based on it's training
- then it will keep predicting until it itself decides to stop
- after stopping it returns the generated tokens and convert back them to text