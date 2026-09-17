import os
import shutil

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse

from langchain_google_genai import ChatGoogleGenerativeAI

from app.rag import ingest_pdf, search_documents, clear_vectorstore


app = FastAPI(
    title="Research Paper Assistant"
)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)



UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>Research Paper Assistant</title>
        </head>

        <body>
            <h1>Research Paper Assistant</h1>

            <h2>Upload Research Papers</h2>

            <form action="/upload" method="post"
                  enctype="multipart/form-data">

                <input
                    type="file"
                    name="files"
                    multiple
                    accept=".pdf"
                />

                <button type="submit">
                    Upload
                </button>

            </form>

            <br>

            <form action="/reset" method="post">
                <button type="submit">
                    Clear All Uploaded Papers
                </button>
            </form>

            <hr>

            <h2>Ask Question</h2>

            <form action="/ask" method="post">

                <input
                    type="text"
                    name="question"
                    placeholder="Ask about your papers"
                    style="width:400px"
                />

                <button type="submit">
                    Ask
                </button>

            </form>

        </body>
    </html>
    """


@app.post("/reset")
async def reset_papers():

    # Clear ChromaDB
    clear_vectorstore()

    # Delete uploaded PDF files
    for filename in os.listdir(UPLOAD_DIR):

        file_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        if os.path.isfile(file_path):
            os.remove(file_path)

    return {
        "message":
        "All uploaded papers and stored document data have been cleared."
    }


@app.post("/upload")
async def upload_papers(
    files: list[UploadFile] = File(...)
):

    uploaded = []
    errors = []

    for file in files:

        if not file.filename.lower().endswith(".pdf"):

            errors.append(
                f"{file.filename}: Only PDF files are supported."
            )

            continue

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        try:

            chunks = ingest_pdf(
                file_path,
                file.filename
            )

            if chunks == 0:

                errors.append(
                    f"{file.filename}: No readable text found."
                )

            else:

                uploaded.append(
                    {
                        "filename": file.filename,
                        "chunks": chunks
                    }
                )

        except Exception as e:

            errors.append(
                f"{file.filename}: {str(e)}"
            )

    return {
        "uploaded": uploaded,
        "errors": errors
    }


@app.post("/ask")
async def ask_question(
    question: str = Form(...)
):

    question = question.strip()

    if not question:

        return {
            "answer": "Question cannot be empty."
        }

    if not os.path.exists(UPLOAD_DIR):

        return {
            "answer":
            "Please upload at least one research paper first."
        }

    pdf_files = [
        f
        for f in os.listdir(UPLOAD_DIR)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:

        return {
            "answer":
            "Please upload at least one research paper first."
        }

    results = search_documents(
        question,
        k=5
    )

    if not results:

        return {
            "answer":
            "The answer is not available in the uploaded documents."
        }

    context_parts = []

    for doc in results:

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        context_parts.append(
            f"Source: {source}, Page: {page}\n"
            f"{doc.page_content}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a Research Paper Assistant.

IMPORTANT RULES:

1. Answer ONLY using the provided context.
2. Do NOT use outside knowledge.
3. Do NOT make up information.
4. If the answer is not present in the context,
   say exactly:

"The answer is not available in the uploaded documents."

5. Include the source document name and page number
   for information used in the answer.

CONTEXT:
{context}

QUESTION:
{question}
"""

    response = llm.invoke(prompt)

    answer = response.content

    if isinstance(answer, list):

        answer = "".join(
            item.get("text", "")
            if isinstance(item, dict)
            else str(item)
            for item in answer
        )

    sources = []

    for doc in results:

        sources.append(
            {
                "document": doc.metadata.get(
                    "source",
                    "Unknown"
                ),
                "page": doc.metadata.get(
                    "page",
                    "Unknown"
                )
            }
        )

    return {
        "answer": answer,
        "sources": sources
    }