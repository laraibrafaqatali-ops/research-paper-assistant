# 📚 Research Paper Assistant

An AI-powered research paper assistant that allows users to upload PDF research papers and search their content using semantic similarity search.

## 🚀 Live Demo

🔗 https://research-paper-assistant-to3a.vercel.app

## 💻 GitHub Repository

🔗 https://github.com/laraibrafaqatali-ops/research-paper-assistant

---

## ✨ Features

* 📄 Upload research paper PDFs
* 🔍 Semantic search across uploaded documents
* 🤖 AI-powered document embeddings
* 🧩 PDF text extraction and chunking
* 🗄️ Vector storage using ChromaDB
* ⚡ Fast similarity-based document retrieval
* ☁️ Deployable on Vercel
* 🧹 Clear and rebuild the vector store

---

## 🧠 How It Works

The application follows a Retrieval-Augmented Generation (RAG)-style document retrieval workflow:

```text
PDF Upload
    ↓
PDF Text Extraction
    ↓
Text Chunking
    ↓
Gemini Embeddings
    ↓
ChromaDB Vector Store
    ↓
User Search Query
    ↓
Semantic Similarity Search
    ↓
Relevant Research Paper Sections
```

The research paper is divided into smaller text chunks. Each chunk is converted into an embedding using Google's Gemini embedding model and stored in ChromaDB.

When a user searches for something, the query is converted into an embedding and the most semantically relevant document chunks are retrieved.

---

## 🛠️ Tech Stack

| Technology | Purpose                           |
| ---------- | --------------------------------- |
| Python     | Backend development               |
| LangChain  | Document processing and retrieval |
| Gemini     | Text embeddings                   |
| ChromaDB   | Vector database                   |
| PyPDF      | PDF document loading              |
| Vercel     | Deployment                        |

---

## 📁 Project Structure

```text
research-paper-assistant/
│
├── app/
│   ├── main.py
│   └── rag.py
│
├── requirements.txt
├── vercel.json
├── README.md
└── ...
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/laraibrafaqatali-ops/research-paper-assistant.git
```

### 2. Navigate to the project

```bash
cd research-paper-assistant
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

The application requires a Google Gemini API key.

Create a `.env` file locally:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

### Vercel

For Vercel deployment, add the following environment variable in:

**Vercel → Project → Settings → Environment Variables**

```text
GOOGLE_API_KEY=your_gemini_api_key
```

> Never commit your API key or `.env` file to GitHub.

---

## ▶️ Running Locally

Start the application using your project's configured command.

For example, if your application uses FastAPI:

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

---

## 🔎 Example Workflow

1. Upload a research paper in PDF format.
2. The application extracts the text.
3. The text is divided into smaller chunks.
4. Gemini generates embeddings for those chunks.
5. The embeddings are stored in ChromaDB.
6. Enter a question or search query.
7. The application finds the most relevant sections of the research paper.

---

## ☁️ Deployment

The project can be deployed using Vercel.

### Basic deployment steps

```bash
git add .
git commit -m "Update project"
git push
```

Connect the GitHub repository to Vercel and configure:

```text
GOOGLE_API_KEY
```

as an environment variable.

---

## ⚠️ Production Note

The current implementation uses:

```text
/tmp/chroma_db
```

for ChromaDB storage when running on Vercel.

Vercel's serverless filesystem is temporary, so uploaded documents and vector data should not be treated as permanent production storage.

For a production application, a persistent vector database or external storage service should be considered.

---

## 🔮 Future Improvements

* 💬 Add an AI chatbot for questions about uploaded papers
* 📚 Support multiple research papers
* 🧠 Generate summaries automatically
* 📝 Generate citations and references
* 🔐 Add user authentication
* ☁️ Use persistent cloud vector storage
* 📊 Add research paper analytics
* 📥 Export generated answers and summaries

---

## 👩‍💻 Author

**Laraib Rafaqat Ali**

GitHub:
https://github.com/laraibrafaqatali-ops

Project:
https://github.com/laraibrafaqatali-ops/research-paper-assistant

Live Demo:
https://research-paper-assistant-to3a.vercel.app

---


