from app.rag.loaders.pdf_loader import load_pdf
from app.rag.chunking.text_splitter import split_documents
from app.rag.vectorstore.chroma_store import create_vector_store
from app.rag.retriever.retriever import retriever_documents

documents = load_pdf("sample.pdf")

chunks = split_documents(documents)

create_vector_store(chunks)

results = retriever_documents("Artificial Intelligence in helthcare?")

for i, doc in enumerate(results, 1):
    print(f"\nChunk {i}")
    print("-"*50)
    print(doc.page_content)