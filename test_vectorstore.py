from app.rag.loaders.pdf_loader import load_pdf
from app.rag.chunking.text_splitter import split_documents
from app.rag.vectorstore.chroma_store import create_vector_store

pdf_path = "sample.pdf"

documents = load_pdf(pdf_path)

chunks = split_documents (documents)

vector_store = create_vector_store(chunks)

print("Vector database created successfully")

results = vector_store.similarity_search("What is Artificial Intelligence?", k = 2)

print("\nRetrieved chunks:\n")

for result in results:
    print(result.page_content)
    print("----------------------------")