🚀 Medical Bill Validation Agent (LLM + RAG + LangGraph)

An end-to-end AI-powered medical bill validation system that uses OCR, LLM-based parsing, and Retrieval-Augmented Generation (RAG) to automatically analyze hospital bills and detect overcharging.

🔥 Features
🧾 OCR Extraction – Extracts text from medical bill images using Tesseract
🧠 LLM Parsing – Converts noisy OCR text into structured JSON
🔍 RAG-based Retrieval – Fetches correct tariff data using vector search (ChromaDB + embeddings)
⚖️ Cost Validation – Compares billed vs actual cost and flags overcharges
🤖 LangGraph Agent – Dynamic agent that decides workflow steps (OCR → Parse → Validate)
🌐 FastAPI Backend – API for real-time bill analysis
🎨 Simple UI – Upload bills and view structured results
🐳 Dockerized – Fully containerized for easy deployment
🧠 Architecture
User Upload (UI)
        ↓
FastAPI Backend
        ↓
LangGraph Agent (LLM Brain)
        ↓
OCR → Parser → RAG → Compare
        ↓
Structured Output (JSON)
🛠️ Tech Stack
LLM & Agents: LangGraph, LangChain
Vector DB: ChromaDB
Embeddings: Sentence Transformers
OCR: Tesseract, OpenCV
Backend: FastAPI
Frontend: HTML + JS
Deployment: Docker
🚀 How to Run
1. Clone repo
git clone <your-repo-url>
cd medical-bill-agent
2. Run with Docker
docker-compose up --build
3. Open UI
http://localhost:8000
🧪 Example Output
[
  {
    "service": "Blood Group",
    "billed": 100,
    "actual_cost": 100,
    "difference": 0,
    "overcharged": false
  }
]
💡 Key Highlights
Built a state-driven AI agent instead of a fixed pipeline
Handles noisy OCR + real-world billing formats
Uses LLM reasoning for dynamic decision-making
Designed for scalability across multiple hospitals
🎯 Use Cases
Insurance claim validation
Hospital billing audits
Healthcare fraud detection
Automated invoice verification
📌 Future Improvements
Multi-agent system (OCR agent, validation agent, reasoning agent)
Confidence scoring & explanation generation
Support for PDFs and multi-page bills
Deployment on cloud (Render / HuggingFace Spaces)

👨‍💻 Author
Deepesh Madane
