# Academic AI Assistant (Local RAG)

Academic AI Assistant is a **locally deployed, privacy-preserving** learning assistant that helps students study from their own documents using **Retrieval-Augmented Generation (RAG)**.

It supports:
- 📄 Document Q&A (answers grounded in your uploaded PDFs/TXT)
- 🧪 Auto Quiz Generation (MCQ + True/False)
- ✍️ Text Summarization
- 🧠 Concept Explanation
- 💬 General Academic Chat

All processing runs **locally** (no cloud API required) using **Ollama + LLM**.

---

## Tech Stack
- **Streamlit** (UI)
- **LangChain** (RAG orchestration)
- **ChromaDB** (vector database)
- **Sentence Transformers** (embeddings)
- **Ollama** (local LLM inference)

---

## Project Structure
academic_ai_assistant/
├── app.py
├── requirements.txt
├── utils/
│ ├── document_processor.py
│ ├── vector_store.py
│ ├── llm_handler.py
│ └── quiz_generator.py
└── data/
├── documents/ # (ignored in git) user uploads
└── vectorstore/ # (ignored in git) chromadb index

## Setup Instructions

### 1) Clone the repo
```bash
git clone https://github.com/<your-username>/academic-ai-assistant.git
cd academic-ai-assistant/academic_ai_assistant

Create a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

Install Ollama + pull model
ollama pull llama3.2:3b
streamlit run app.py

