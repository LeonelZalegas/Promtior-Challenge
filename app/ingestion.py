import os
from pathlib import Path

from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma


PROMTIOR_URL = "https://promtior.ai/"
EXTRA_PDF    = "ExtraInfo.pdf"      
DB_DIR       = Path("db")
CHUNK_SIZE   = 1000
CHUNK_OVERLAP = 150


def collect_documents() -> list[Document]:
    docs: list[Document] = []

    web_loader = WebBaseLoader(PROMTIOR_URL)
    docs.extend(web_loader.load())

    pdf_loader = PyPDFLoader(EXTRA_PDF)
    docs.extend(pdf_loader.load())

    return docs


def build_vectorstore(docs: list[Document]) -> None:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=str(DB_DIR)
    )
    print(f"Vector store generado en {DB_DIR}/")


if __name__ == "__main__":
    if DB_DIR.exists():
        print("El Vector Store ya existe capo")
    else:
        documents = collect_documents()
        build_vectorstore(documents)
