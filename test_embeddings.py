from app.rag.embeddings.embedding_model import get_embedding_model

embedding_model = get_embedding_model()

text = "Artificial Intelligence is transforming technology"

vector = embedding_model.embed_query(text)

print("Embedding generated successfully")

print("Vector lenght:", len(vector))

print("First 10 value: ")

print(vector[:10])