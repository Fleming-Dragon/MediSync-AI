# 🩺 MediSync AI  
**Agentic RAG System for Medical Decision Support**

MediSync AI is an **agent-based medical assistant** built with **LangGraph, LangChain, Streamlit, and Groq LLMs**.  
It combines **retrieval-augmented generation (RAG)** from a trusted medical PDF, **self-grading logic**, **web fallback search**, and **medical image analysis** into a single interactive application.

> **Disclaimer**  
> This project is a **clinical decision-support tool** for educational and professional use.  
> It **does not provide medical diagnoses** and must not replace licensed medical judgment.

---

## Features

- **Medical Knowledge Base (RAG)**
  - Indexed from *The Gale Encyclopedia of Medicine (3rd Edition)*
  - Stored locally using **ChromaDB**
- **Self-Correcting Agent**
  - Grades PDF relevance before answering
  - Automatically falls back to **web search** when needed
- **Web Search Integration**
  - Uses DuckDuckGo for up-to-date medical information
- **Medical Image Analysis**
  - Supports X-ray / MRI image uploads
  - Vision model describes findings *without diagnosis*
- **Chat-Based Streamlit UI**
  - Session-based history
  - Clear source attribution (PDF vs Web)
- **Powered by Groq**
  - Llama 3.3 70B for reasoning
  - Llama 4 Maverick 17B for vision

---

## Project Structure

```text
.
├── app.py            # Streamlit UI and application entry point
├── agent.py          # Agentic RAG workflow (LangGraph)
├── retriever.py      # PDF ingestion and vector retrieval (ChromaDB)
├── requirements.txt  # Python dependencies
├── .env              # Environment variables (Groq API Key)
└── chroma_db_data/   # Persisted vector database (auto-generated)
```

---

## Running MediSync AI Locally
This guide explains how to set up and run **MediSync AI** on your local machine. 

> **Note**  
> The instructions below assume you are using a **Linux-based system**.  
> Commands may differ slightly on **Windows** or **macOS**.

Before starting, create an account at **groq.com** and generate a **Groq API key**, which will be required to run the application.

### Prerequisites
Ensure you have the following installed on your machine:

- **Python 3.12 or higher**
- **python3-venv**
- **pip**

### 1. Navigate to the Project Directory
```bash
cd MediSync-AI
```

### 2. Create a Virtual Environment
Create an isolated Python environment for dependency management:
```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment
Activate the environment:
```bash
source venv/bin/activate
```
Your terminal prompt should now indicate that the virtual environment is active.

### 4. Install Project Dependencies
Install all required Python packages:
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a ```.env``` file at the root of the project:
```bash
touch .env
```
Add your **Groq API key** key to the file:
```bash
GROQ_API_KEY="your_groq_api_key_here"
```
Ensure this file is not committed to version control.

### 6. Launch the Application
Start the Streamlit application:
```bash
streamlit run app.py
```
Once launched, Streamlit will display a **local URL** (typically http://localhost:8501) where you can access the MediSync AI interface in your browser.

