# Text Chunking Strategies

### Q1. Explain why it's necessary to break down large documents into smaller chunks in a RAG pipeline?

- let's suppose there is a large text / document, to findout an single fact from that big text, we've to send that entire text/doc to the model , then the model will read entire doc then will give answer , but that's WASTAGE OF INPUT TOKENS , so to save token usage we can breakdown into chunks (i.e. smal parts) nd avoid sending unnecessary information to the model, which can be costly and slow. Then the model will findout the best matching chunk where out answer can be present the will accept that chunk only nd then will give response

### Q2. what are some different strategies or methods you can use to perform this text chunking?

- size based, semantic based, & structure based chunking

### Q3. Could you elaborate a bit on what each of these strategies entails? For example, what does "size-based chunking" mean in practice?

- For size-based chunking, it involves cutting text into pieces based on a fixed number of tokens or characters. This is straightforward but can sometimes cut sentences or ideas in half.

- For structure-based chunking, splitting by headers, sections, or paragraphs is indeed a very effective way to keep related information together.

- Semantic chunking leverages NLP techniques to group related sentences. It's about identifying the natural breaks in meaning within a text, rather than just arbitrary size limits or predefined structural elements.

# Text Embeddings

### Q4. Explain what text embeddings are and why they are crucial for semantic search in a RAG pipeline?

- embeddings convert text into a "numeric version" of each chunk, and that these numerical representations are crucial for semantic search.
- those numericals are typically high-dimensional vectors, and the specific range of numbers can vary depending on the embedding model used.
- nd in semanic search it used to split sentences based on related sentences nd by finding out natual stoppages among lines, after converting each chunk to numbers , whenever user will ask a qn, model will search most matchable embedding for that question's embedding with the pre ceated embedding of the dataset which would be present in vector database

### Q5. How does comparing these numerical representations (embeddings) allow the system to find the "most matchable" chunk for a user's question?

- for semantic serach / finding matches it uses a method called cosine similarity.
- that means it findsout the cosine angle between query vector and document chunk vectors.
- A cosine value close to 1 indicates high similarity, while values closer to 0 (or negative) indicate less similarity or even opposing meanings.

# RAG Pipeline Implementation

### Outline the basic steps involved in building a RAG workflow, from a user asking a question to the model generating a response !

```
Documents → Chunks → Numbers → Vector DB
                        ↓
Question → Numbers → SEMANTIC SEARCH → Best Matches → LLM → Answer!
```

### Now, let's think about the practical aspects of putting this into action. When you're implementing this RAG workflow, what are some of the key components or tools you would need to set up and integrate?

- first of all manually create a function or use laregly used frameorks like langchain / llamaindex, which will breakdown out document of large text into chunks using whatever strategy we wanna use for makin chunks
- Then i'll use vector database, which is specifically designed to store and efficiently query these high-dimensional embeddings. This is a crucial component for enabling fast and accurate semantic search in your RAG pipeline.
- Then for converting chunks -to-> embeddings , we can use voyage ai / openai (paid), Fastembd (free), then at the end use AI MODEL for generating

# Optimizing RAG Performance

### When you're trying to make your RAG system perform better, what are some of the parameters or aspects you might consider tuning or adjusting?

- To optimize RAG, tune these in order:
  1. Chunk size & overlap (get the pieces right)
  2. Top-K & threshold (get the right number of pieces)
  3. Embedding model (get better quality pieces)
  4. Hybrid search & diversity (get varied pieces)
  5. Prompt (use the pieces well)

### Chunk size and overlap. Why are these two parameters so important, and what are the trade-offs you might consider when deciding on their values?

- chunk size matters cuz, if we'll do too small chunk then will get crumbs i.e. no context, for too big chunk we'll get the more than the necessary context i.e. too much noise, for just right chunks we'll get enough context , which is not too much noise

- overlap is also imp cuz for 0% overlap there is no duplicates but it might miss the real context boundary, for 10-20% overlap it will contain some reasonable duplicates which is good for context preservation, for 30%+ overlap it is excellent context flow nd will never miss boundaries but a lots of duplicates, waste of money

> **This deep understanding of chunking parameters is vital for Optimizing RAG Performance.**

# Identifying RAG Failure Modes: Recognizing and solving common issues in RAG systems.
