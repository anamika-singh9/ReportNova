from app.rag.loaders.pdf_loader import load_pdf

pdf_path = "sample.pdf"

documents= load_pdf(pdf_path)

print("Number of pages: ", len(documents))

print("\nFirst page content:\n")

print(documents[0].page_content[:500])