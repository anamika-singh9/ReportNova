from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path):
    """
    Load PDF document and return pages.
    """

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    return documents