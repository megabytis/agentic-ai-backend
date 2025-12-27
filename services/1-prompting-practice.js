const message1 =
  "You should express what you want a model to do by providing instructions that are as clear and specific as you can possibly make them. This will guide the model towards the desired output, and reduce the chances of receiving irrelevant or incorrect responses. Don't confuse writing a clear prompt with writing a short prompt. In many cases, longer prompts provide more clarity and context for the model, which can lead to more detailed and relevant outputs.";
const prompt1 = `Summarize the text delimited by double quote into a single sentence. 
"${message1}"
`;

const prompt2 =
  "Generate a list of three made-up book titles along with their authors and genres. Provide them in JSON format with the following keys: book_id, title, author, genre.";

const message2 = `Making a cup of tea is easy! First, you need to get some water boiling. While that's happening, grab a cup and put a tea bag in it. Once the water is hot enough, just pour it over the tea bag. Let it sit for a bit so the tea can steep. After a few minutes, take out the tea bag. If you like, you can add some sugar or milk to taste. And that's it! You've got yourself a delicious cup of tea to enjoy.`;
const prompt3 = `
You will be provided with text delimited by triple double-quotes. 
If it contains a sequence of instructions, re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, then simply write "No steps provided".

"""${message2}"""
`;

const message3 = `
The sun is shining brightly today, and the birds are singing. It's a beautiful day to go for a walk in the park. The flowers are blooming, and the trees are swaying gently in the breeze. People are out and about, enjoying the lovely weather. Some are having picnics, while others are playing \ 
games or simply relaxing on the grass. It's a perfect day to spend time outdoors and appreciate the beauty of nature.
`;
const prompt4 = `
You will be provided with text delimited by triple double-quotes. 
If it contains a sequence of instructions, re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, then simply write "No steps provided."

"""${message3}"""
`;

const prompt5 = `
Your task is to answer in a consistent style.

<child>: Teach me about patience.

<grandparent>: The river that carves the deepest valley flows from a modest spring; the grandest symphony originates from a single note; the most intricate tapestry begins with a solitary thread.

<child>: Teach me about resilience.
`;

const message4 = `
In a charming village, siblings Jack and Jill set out on a quest to fetch water from a hilltop well. As they climbed, singing joyfully, misfortune struck—Jack tripped on a stone and tumbled down the hill, with Jill following suit. Though slightly battered, the pair returned home to comforting embraces. Despite the mishap, their adventurous spirits remained undimmed, and they continued exploring with delight.
`;
const prompt6 = `
Perform the following actions:
1 - Summarize the following text delimited by triple backticks with 1 sentence.
2 - Tranlate the summary into Latin.
3 - List each name in the Latin summary.
4 - Output a JSON object that contains the follwing keys: latin_sumamry, num_names

Use the following format:
Text: <text_to_summerize>
Summary: <summary>
Translation: <summary_translation>
Names: <list_of_names_in_latina_summary>
output JSON: <json_with_summary_and_num_names>

Text to summarize:
\`\`\`${message4}\`\`\`
`;

const prompt7 = `
Your task is to determine wheather the student's solution is corerct or not.
To solve the problem do the following ;
- First, workout your own solution to the problem including the final total price.
- Then compare your solution to the student's solution and evaluate if the student's solution is correct or not.
Don't decide if the student's solution is correct until you have done the problem yourself.

Use the follwing format:
Question: 
\`\`\`<question_here>\`\`\`

Student's solution:
\`\`\` Student's solution here \`\`\`

Actual Solution:
\`\`\` steps to workout the solution and your solution here \`\`\`

Is the student's solutin the same as the actual solution you just calculated:
\`\`\` yes or no \`\`\`

Student's Grade:
\`\`\` correct or incorrect \`\`\`

Question:
I'm building a solar power installation and I need help working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost me a flat $100k per year, and an additional $10 / squarefoot What is the total cost for the first year of operations 
as a function of the number of square feet.

Student's Solution:
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
`;

const prompt8 = "Tell me about 2mm thin invisible wooden door!"; // hallucinating prompt :)

const response = await fetch("http://localhost:11434/api/generate", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    model: "gemini-3-flash-preview:cloud",
    prompt: `${prompt8}`,
    stream: false,
  }),
});

const data = await response.json();
console.log(data.response);
