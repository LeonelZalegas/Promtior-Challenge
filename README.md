## **Project Overview**

To approach thiss challenge effectively, I knew I needed to get started by investigating the RAG architecture theory and the technologies involved. I spent time reviewing the official documentation for LangChain basically, and understanding the core values of RAG.

At the beginning I understood each step in the theory, how there was an Indexing (offline) part and then Retrieval + Generation (online) and the sequential steps in each of them and how they worked under the hood. Initially I thought we needed to make all the steps manually by code but then realized that LangChain and other tools (RetrievalQA, etc) were just doing most of the work automatically, especially the “online” part thanks to the Chains.

## Implementation

Everything starts with the **Document Ingestion and Processing.** Documents are taken from the official Promtior web page and the PDF you guys shared (only the parts that matter actually), using LangChain's loaders (WebBaseLoader and PyPDFLoader).

Then these documents are chunked (at the beginning I was playing around with the size and overlap values as also researching the default values and figured out that 1000 and 150 were good enough) and then vectorized them all (using the GoogleGenerativeAIEmbedding embedding) and created the vector store with Chroma. 

<br>

When it comes to the **Retrieval and Generation**, what I did was loading the vector store again, building the prompt (again, tried with different prompts and this one seems to work better, since it avoids the LLM to hallucinate in case it doesn't know about something).

Finally we generate the chain itself (I used RetrievalQA), I have used a k=3 (meaning it’s gonna use like the top 3 of the most similar vectors in the vector store for the processing of the prompt vectors) and also I have used Gemini as for the LLM. Have noticed that langchain_google_genai was released at the end of May so since I already had a token for the Gemini API I just used it.  

<br>

As for the **Frontend and Deployment** I have used a simple but effective frontend (HTML/CSS/JS) that interacts with the FastAPI backend through REST calls. In here I kinda used the o4 model for making the frontend a lil better and cooler. The project is containerized using Docker and deployed first on AWS App Runner, and then using Railway (never used it so wanted to know how fast could you do it hehe). When it comes to the AWS deployment I have used Amazon ECR, the container registry.

## Main Challenges Encountered and Solutions

One significant challenge encountered was related to caching responses to optimize performance and reduce redundant API calls. Initially, I wanted to utilize LangChain’s built-in caching mechanism with SQLite to store and retrieve cached responses. However, I found that at the current date, the ChatGoogleGenerativeAI component of LangChain does not support internal cache queries, unlike its OpenAI and Anthropic counterparts.

As a workaround, I implemented a simple in-memory dictionary cache to store query-response pairs temporarily. But to be honest I didn’t like the idea since the cache does not persist across application restarts and also it was just not an efficient solution overall. So at the end of the day I just discarded it.

There were other minor problems like realizing that the dependencies versions were not compatible in some versions, or that I forgot that AWS/Railway can’t read variables in **build** time (just in **runtime**), etc. But didn’t take too much time to solve them.


## Links

### AWS (container registry)
https://yjszsguzeg.us-east-2.awsapprunner.com/

### Railway
https://promtior-challenge-production-79f9.up.railway.app/
