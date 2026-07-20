from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import settings

def get_gemini_model():
    """
    Create and return a Gemini model.
    """
    model = ChatGoogleGenerativeAI(
        model = settings.GOOGLE_MODEL, 
        google_api_key = settings.GOOGLE_API_KEY, 
        temperature= settings.TEMPERATURE,
    )
    return model