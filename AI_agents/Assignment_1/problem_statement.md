Enterprise AI Knowledge Assistant with RAG and Web API
------------------------------------------------------

**Build a company knowledge assistant that can answer staff questions based on internal documents using FastAPI, LangChain, an LLM, and a Vector Database.**

### Goal

Create a production-style AI backend system that allows users to upload organizational documents and then query them using natural language. The system must retrieve relevant knowledge and generate accurate responses, not hallucinations.

### Core Functional Requirements

1.  A FastAPI backend service that exposes API endpoints.
    
2.  Endpoint to upload organization documents (text, PDF converted to text manually acceptable).
    
3.  Documents must be embedded and stored in a vector database.
    
4.  When a user asks a question, the system should:
    
    1.  Retrieve relevant content from the vector database
        
    2.  Generate final response via LLM
        
    3.  Respond using RAG formatting
        
5.  Each answer must reference the document sources used.
    

### Technical Requirements

*   Backend Framework : **FastAPI**
    
*   Database : PostgreSQL for storing metadata such as:
    
    *   Document name
        
    *   Upload date
        
    *   Embedded chunk references
        
    *   Usage logs
        
*   Vector Database :  Any one of the following:
    
    *   Chroma
        
    *   FAISS
        
    *   PgVector extension in PostgreSQL
        
*   LLM Integration : OpenAI
    
*   LangChain Usage : Use LangChain for:
    
    *   Embedding
        
    *   Vector storage
        
    *   Retrieval
        
    *   Prompt template
        
    *   Final answer chain
        

**Expected API Endpoints**

*   Upload Document
    
*   Query Question
    
*   List Uploaded Documents
    
*   View Query Logs
    

### Functional Flow

User uploads a file → System chunks + embeds text → Stores in vector DB → User asks a question → System retrieves relevant sections → LLM generates contextual answer.

**Expected Output Format (Example)**

*   Answer section
    
*   Referenced document sections
    
*   Confidence score
    

**Additional Expectations**

*   Stable reasoning
    
*   Responses should not hallucinate
    
*   System must reject questions if no relevant information is found and respond:
    
    *   “No matching information identified. Please upload relevant documents.”
        

#### Logging Requirements

Store each question and answer in PostgreSQL including:

*   Timestamp
    
*   Document IDs used
    
*   Tokens consumed (optional)
    
*   Response accuracy (self-rated)
    
*   Chunk size and overlap must be thoughtfully chosen for reliability.
    

**What Will Be Observe**

*   Robust design
    
*   Correct chaining
    
*   Database usage
    
*   Clear prompts
    
*   Reliability under different queries
    
*   Ability to handle empty or irrelevant input gracefully