import os
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate

DB_DIR = Path("db")

def _load_vector():
    if not DB_DIR.exists():
        raise RuntimeError(
            "Vector DB no encontrado. Hay que correr `python -m app.ingestion` 1eroo"
        )
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return Chroma(
        persist_directory=str(DB_DIR),
        embedding_function=embeddings,
    )

def _build_prompt():
    return ChatPromptTemplate.from_messages([
        ("system",
         "Sos un asistente útil de Promtior. "
         "Responde SOLO con la información del contexto. "
         "Si la respuesta no está, contesta 'No dispongo de esa información'.\n\n"
         "{context}"),
        ("human", "{question}")
    ])

def get_rag_chain():
    vector = _load_vector()
    retriever = vector.as_retriever(search_kwargs={"k": 3})

    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GENAI_MODEL", "gemini-1.5-flash-latest"),
        temperature=0
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": _build_prompt()},
        return_source_documents=True,
        input_key="question" 
    )
    return qa_chain
