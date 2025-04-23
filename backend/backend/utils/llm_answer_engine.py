import requests

def generate_answer_with_mistral(question, context_chunks):
    context = "\n".join(context_chunks)

    prompt = f"""
You are an intelligent assistant. Use only the following context to answer the question.
If the answer cannot be found in the context, say "I don't know."

Context:
\"\"\"
{context}
\"\"\"

Question: {question}

Answer:
"""

    print("📨 Sending prompt to LLaMA:\n", prompt)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3  # 🔥 Controlled, deterministic
                }
            },
            timeout=120  # Long enough for large documents
        )
        response.raise_for_status()
        return response.json().get("response", "No response from LLaMA.")
    except requests.exceptions.RequestException as e:
        return f"❌ Failed to connect to LLaMA: {str(e)}"
