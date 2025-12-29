import validator from "validator";
import { JSDOM } from "jsdom";
import { Readability } from "@mozilla/readability";
import dotenv from "dotenv"
dotenv.config()

const url = `https://sleepyclasses.com/womens-safety-in-india/`;

if (!validator.isURL(url)) {
  throw new Error("Invalide URL!");
}

const htmlRes = await fetch(url);
const html = await htmlRes.text();

const dom = new JSDOM(html, { url });

const readableContent = new Readability(dom.window.document);
const article = readableContent.parse();

if (!article || !article.textContent) {
  throw new Error("Could not be able to extract article's content!");
}

const articleText = article.textContent.trim();

const MAX_CHAR = 5000;
const cleanText = articleText.slice(0, MAX_CHAR);

const response = await fetch(LOCALHOST_OLLAMA_GENERATE_API, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    model: "gemini-3-flash-preview:cloud",
    prompt: `Summarize the following article :
     """
     ${cleanText}
     """

     important points to note :
     1. summary should be in points like point 1, 2, 3 like this....
     2. provide strict 5 points which should describe complete meaning of the entire paragraph
     3. language should be very simple, understandable english
     `,

    stream: false,
  }),
});

const data = await response.json();
console.log(data.response);
