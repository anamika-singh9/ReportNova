from app.rag.loaders.pdf_loader import load_pdf
from app.rag.chunking.text_splitter import split_documents
from app.rag.vectorstore.chroma_store import create_vector_store
from app.utils.logger import logger
from app.rag.retriever.retriever import retriever_documents


def process_pdf(pdf_path: str):
    """
    Complete RAG indexing pipeline.

    PDF
        ↓
    Loader
        ↓
    Chunker
        ↓
    Embeddings
        ↓
    Chroma
    """

    logger.info("Loading PDF.")

    # Step 1
    documents = load_pdf(pdf_path)

    logger.info("Splitting document into chunks.")

    # Step 2
    chunks = split_documents(documents)

    logger.info("Creating vector database.")

    # Step 3
    create_vector_store(chunks)

    logger.info("Vector database created successfully.")

    return len(chunks)


def retrieve_context(query: str) -> str:
    """
    Retrieve relevant context from the indexed PDF.
    """

    documents = retriever_documents(query)

    if not documents:
        return ""

    context = []

    for doc in documents:
        context.append(doc.page_content)

    return "\n\n".join(context)