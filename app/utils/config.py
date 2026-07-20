
from config.settings import settings

def show_config():
    print("Application:", settings.APP_NAME)
    print("Environment:", settings.ENVIRONMENT)
    print("OpenAI Key Available:", bool(settings.OPENAI_API_KEY))
    print("Google Key Available:", bool(settings.GOOGLE_API_KEY))
    print("Tavily Key Available:", bool(settings.TAVILY_API_KEY))