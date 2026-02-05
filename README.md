# 📊 Financial Document Q&A Assistant

A **ChatGPT-like conversational assistant** that allows users to upload **financial Excel or PDF documents** and ask questions about them.  
The system is designed to be **fast, accurate, and reliable**, especially for numerical financial data.

---

## ✨ Features

- 📁 Upload **Excel (`.xlsx`, `.xls`) or PDF** financial documents  
- 💬 **ChatGPT-style conversational interface** (fixed bottom search bar with send arrow)
- ⚡ **Instant & accurate numeric answers** from Excel files  
- 🤖 AI-powered explanations using **Ollama (local LLM)**
- 🧠 **Conversation memory** for follow-up questions (e.g., *“why?”*, *“explain that”*)
- 🔒 Deterministic design — **financial numbers never come from the LLM**
- 🖥️ Runs completely **locally** (no external APIs)

---

## 🧠 Design Philosophy

Large Language Models are not reliable for exact numerical retrieval.  
This project follows a **hybrid architecture**:

- **Python logic** handles:
  - Excel parsing
  - Numeric lookups
  - Comparisons and calculations  
- **Local LLM (Ollama)** handles:
  - Explanations
  - Summaries
  - Conversational responses  

This ensures:
- ✅ No hallucinated numbers  
- ⚡ Fast responses  
- 💬 Natural, ChatGPT-like interaction  

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – UI & chat interface
- **Pandas** – Excel processing
- **PyPDF2** – PDF text extraction
- **Ollama** – Local LLM runtime
- **phi3:mini** (lightweight model)

---

## 📁 Project Structure
financial_qa_app/
│
├── app.py
├── utils/
│   ├── document_processing.py
│   ├── answer_router.py
│   └── ollama_integration.py
├── requirements.txt
└── README.md

---

## 🚀 How It Works

1. Upload a financial document (Excel or PDF)
2. Excel files are parsed into structured Python dictionaries
3. Ask questions using a chat interface
4. The system routes questions automatically:
   - **Numeric / factual → Python (instant & exact)**
   - **Explanatory / follow-up → Ollama**
5. Previous answers remain visible and are used for conversational context

---

## 📊 Example Questions

- What are the total assets for 2023?
- What are the total liabilities for 2022?
- Compare assets and liabilities
- Why is this important?
- Explain the financial position in simple terms

---

## 🧪 Running the App Locally

### 1️⃣ Clone the repository
```bash
git clone <your-repo-url>
cd financial_qa_app
---
---
### 2️⃣ Create & activate virtual environment
