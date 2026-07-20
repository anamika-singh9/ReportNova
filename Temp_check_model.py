from google import genai
from config.settings import settings

client=genai.Client(api_key=settings.GOOGLE_API_KEY)
for model in client.models.list():
    print(model.name)