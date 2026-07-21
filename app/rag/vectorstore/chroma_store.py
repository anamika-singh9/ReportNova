from langchain_chroma import Chroma
from app.rag.embeddings.embedding_model import get_embedding_model

PERSIST_DIRECTORY = "./chroma_db"


def create_vector_store(chunks):
    embeddings = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )

    return vector_store


def load_vector_store():
    embeddings = get_embedding_model()

    vector_store = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )

    return vector_store