from app.rag.loaders.pdf_loader import load_pdf
from app.rag.chunking.text_splitter import split_documents

pdf_path = "sample.pdf"

documents = load_pdf(pdf_path)

chunks = split_documents(documents)

print("Total pages: ", len(documents))

print("Total chunks: ", len(chunks))

print("\nFirst Chunk:\n")

print(chunks[0].page_content)