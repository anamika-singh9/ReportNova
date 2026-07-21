from app.rag.vectorstore.chroma_store import load_vector_store


def get_retriever():
    """
    Create and return a retriever from the vector database.
    """

    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    return retriever


def retriever_documents(query: str):
    """
    Retrieve the most relevant document chunks.
    """

    retriever = get_retriever()

    documents = retriever.invoke(query)

    return documents