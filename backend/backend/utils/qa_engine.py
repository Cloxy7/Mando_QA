import openai
from utils.embedding_engine import model  # This is your SentenceTransformer

openai.api_key = "YOUR_API_KEY"  # Replace with your key or load from .env

def retrieve_relevant_chunks(question, semantic_index, top_k=5):
    query_embedding = model.encode([question])[0]
    return semantic_index.search(query_embedding, top_k)

def answer_question(question, semantic_index, top_k=5):
    top_chunks = retrieve_relevant_chunks(question, semantic_index, top_k)
    context = "\n\n".join(top_chunks)

    prompt = f"""Use only the context below to answer the question.

Context:
{context}

Question: {question}

Answer:"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']
