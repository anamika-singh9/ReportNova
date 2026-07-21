from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from config.settings import settings

def get_embedding_model():
    """
    Create and return embedding model.
    """
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key = settings.GOOGLE_API_KEY
    )
    return embeddings