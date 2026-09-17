import os

from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


load_dotenv()


CHROMA_DIR = "./chroma_db"


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)


vectorstore = Chroma(
    collection_name="research_papers",
    embedding_function=embeddings,
    persist_directory=CHROMA_DIR,
)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
)


def ingest_pdf(file_path: str, filename: str):

    reader = PdfReader(file_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text and text.strip():

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": filename,
                        "page": page_number,
                    },
                )
            )

    if not documents:
        return 0

    chunks = text_splitter.split_documents(documents)

    vectorstore.add_documents(chunks)

    return len(chunks)


def search_documents(question: str, k: int = 5):

    results = vectorstore.similarity_search(
        question,
        k=k
    )

    return results


def clear_vectorstore():

    global vectorstore

    vectorstore.delete_collection()

    vectorstore = Chroma(
        collection_name="research_papers",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )