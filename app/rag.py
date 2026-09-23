import os

import chromadb
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# ============================================================

# Gemini API Key

# ============================================================

GOOGLE_API_KEY = (
os.getenv("GOOGLE_API_KEY")
or os.getenv("GEMINI_API_KEY")
)

if not GOOGLE_API_KEY:
raise RuntimeError(
"GOOGLE_API_KEY or GEMINI_API_KEY environment variable is not set."
)

# ============================================================

# Gemini Embeddings

# ============================================================

embeddings = GoogleGenerativeAIEmbeddings(
model="models/text-embedding-004",
google_api_key=GOOGLE_API_KEY,
)

# ============================================================

# ChromaDB

# ============================================================

# Vercel serverless environment mein local persistent

# storage par depend nahi kar rahe.

client = chromadb.Client()

vectorstore = Chroma(
client=client,
collection_name="research_papers",
embedding_function=embeddings,
)

# ============================================================

# PDF Ingestion

# ============================================================

def ingest_pdf(file_path: str, filename: str):
loader = PyPDFLoader(file_path)

```
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

chunks = text_splitter.split_documents(docs)

for chunk in chunks:
    chunk.metadata["source"] = filename

if chunks:
    vectorstore.add_documents(chunks)

return len(chunks)
```

# ============================================================

# Search Documents

# ============================================================

def search_documents(query: str, k: int = 5):
return vectorstore.similarity_search(
query,
k=k,
)

# ============================================================

# Clear Vector Store

# ============================================================

def clear_vectorstore():
global vectorstore

```
try:
    client.delete_collection("research_papers")
except Exception:
    pass

vectorstore = Chroma(
    client=client,
    collection_name="research_papers",
    embedding_function=embeddings,
)
```
