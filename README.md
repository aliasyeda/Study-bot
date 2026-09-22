# StudyBot – AI Study Assistant

An AI-powered study assistant built with Python and FastAPI that provides contextual answers to study-related questions while maintaining persistent conversation history using MongoDB Atlas.

StudyBot integrates an LLM through Groq, exposes RESTful APIs through FastAPI, stores conversation history in MongoDB, and is deployed as a live application on Render.

## Live Demo

**API Base URL:**  
https://study-bot-aliasyeda-duva.onrender.com

**GitHub Repository:**  
https://github.com/aliasyeda/Study-bot

---

## Overview

StudyBot is designed to provide students with an AI-powered conversational interface for asking study-related questions.

Unlike a basic stateless chatbot, StudyBot maintains conversation context by storing chat history in MongoDB Atlas. When a user continues a conversation, previous messages from the session are retrieved and provided as context to the language model.

The application demonstrates the integration of:

- Large Language Models
- REST APIs
- Conversational AI
- Persistent memory
- Database integration
- AI application workflows
- Cloud deployment

---

## Key Features

- AI-powered responses to academic and general study questions
- Context-aware conversations
- Persistent conversation memory
- Session-based chat management
- MongoDB-backed chat history
- RESTful API architecture
- FastAPI Swagger/OpenAPI documentation
- Health-check endpoint
- Chat history retrieval
- Session deletion
- Cloud deployment using Render

---

## Architecture

```text
User
  │
  ▼
FastAPI REST API
  │
  ├── Session Management
  │
  ├── MongoDB Atlas
  │       │
  │       └── Persistent Chat History
  │
  ▼
LangChain
  │
  ▼
Groq API
  │
  ▼
Llama 3.3 70B
  │
  ▼
Context-aware AI Response

The application connects the API layer, conversation memory, database, and LLM into a single AI workflow.
---
## Technology Stack
Technology	Purpose
Python	Application development
FastAPI	REST API backend
Uvicorn	ASGI server
Groq	LLM API provider
Llama 3.3 70B	Language model
LangChain	LLM application integration
MongoDB Atlas	Persistent conversation storage
PyMongo	MongoDB database driver
Render	Cloud deployment
How Conversation Memory Works

StudyBot uses MongoDB Atlas to maintain persistent conversation history.

The workflow is:

A user sends a message through the /api/chat endpoint.
The application checks whether a session_id already exists.
If no session exists, a new UUID is generated.
The most recent messages from the session are retrieved from MongoDB.
Previous messages are formatted and provided to the LLM together with the new question.
The LLM generates a response using the conversation context.
The user message and assistant response are stored in MongoDB.
Database indexes on session_id and timestamp support efficient retrieval.

This allows the assistant to maintain context across interactions instead of treating every question as an isolated request.

## Database Structure

The application stores conversation data in a MongoDB collection named:

chat_history

A simplified document structure is:

{
  "session_id": "unique-session-id",
  "user_id": "student123",
  "messages": [
    {
      "role": "user",
      "content": "What is machine learning?",
      "timestamp": "..."
    },
    {
      "role": "assistant",
      "content": "Machine learning is...",
      "timestamp": "..."
    }
  ],
  "created_at": "...",
  "updated_at": "..."
}

Indexes are created for:

session_id
timestamp
API Endpoints
1. Chat
POST /api/chat

Example request:

{
  "user_id": "student123",
  "message": "What is quantum physics?",
  "session_id": null
}

The endpoint returns the generated response together with the session information.

2. Get Chat History
GET /api/chat/history/{session_id}

Retrieves the stored conversation history for a session.

3. Delete Session
DELETE /api/chat/session/{session_id}

Deletes the stored conversation associated with a session.

4. Health Check
GET /health

Returns the application and database health status.

Example:

{
  "status": "healthy",
  "database": "connected"
}
Example API Request

Using cURL:

curl -X POST "https://study-bot-aliasyeda-duva.onrender.com/api/chat" \
-H "Content-Type: application/json" \
-d '{"user_id":"student","message":"What is artificial intelligence?"}'

Using Python:

import requests

response = requests.post(
    "https://study-bot-aliasyeda-duva.onrender.com/api/chat",
    json={
        "user_id": "test",
        "message": "Explain neural networks"
    }
)

print(response.json()["response"])
Example Questions
---
## StudyBot can be tested with questions such as:

What is the theory of relativity?
Explain how photosynthesis works.
What are the three laws of motion?
Tell me about the Roman Empire.
How do I solve quadratic equations?
Explain artificial intelligence.
What is machine learning?
Running Locally
1. Clone the repository
git clone https://github.com/aliasyeda/Study-bot.git
cd Study-bot
2. Create a virtual environment
python -m venv venv

Activate it on Windows:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file:

GROQ_API_KEY=your_groq_api_key
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=study_bot
COLLECTION_NAME=chat_history

Never commit API keys, database credentials, passwords, or other secrets to GitHub.

5. Start the application
uvicorn main:app --reload

The API will be available locally through the configured FastAPI server.

FastAPI's interactive API documentation can be accessed through:

/docs

---
## Deployment

The application is deployed on:

Render

Live API:

https://study-bot-aliasyeda-duva.onrender.com

Environment-specific credentials such as API keys and database connection strings are configured through deployment environment variables rather than stored in the source code.
---

## Deployment Challenges

During deployment and testing, several practical issues were addressed, including:

Python package compatibility
MongoDB SSL connection issues
Render outbound IP access and MongoDB configuration
Authentication configuration
Port binding
Cloud deployment configuration

These issues provided practical experience with deploying and debugging an AI-backed API application.

---

## Project Highlights

## This project demonstrates hands-on experience with:

AI application development
LLM API integration
Conversational AI
Agentic/workflow-oriented application design
REST API development
Persistent conversational memory
Database integration
Backend development with FastAPI
Cloud deployment
API testing and debugging
Future Improvements

---

## Potential future improvements include:

Adding authentication and user accounts
Supporting document-based question answering
Adding retrieval-augmented generation (RAG)
Integrating educational document uploads
Adding streaming responses
Adding structured study plans
Adding automated quiz generation
Adding additional AI-powered study workflows
Improving observability and error handling
Author

Syeda Alia Samia
