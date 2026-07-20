from app.llms.gemini import get_gemini_model

def get_model(model_name="gemini"):
    """
    Return the requested LLM.
    """

    if model_name =="gemini":
        return get_gemini_model()
    
    raise ValueError(f"Unsupported model: {model_name}")