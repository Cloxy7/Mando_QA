from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from utils.file_type_detector import detect_and_parse
from utils.chunking import chunk_text
from utils.embedding_engine import get_embeddings
from utils.semantic_index import SemanticSearchIndex
from utils.qa_engine import retrieve_relevant_chunks
from utils.llm_answer_engine import generate_answer_with_mistral

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "✅ Mando QA backend is running!"

@app.route('/ask', methods=['POST'])
def ask():
    if "file" not in request.files or "question" not in request.form:
        return jsonify({"error": "Missing file or question"}), 400

    file = request.files["file"]
    question = request.form["question"]

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    print(f"📄 File saved to: {file_path}")
    print(f"❓ Question received: {question}")

    try:
        content = detect_and_parse(file_path)
        print(f"📚 Extracted content length: {len(content)}")

        chunks = chunk_text(content)
        print(f"🔪 Chunked into {len(chunks)} pieces")

        embeddings = get_embeddings(chunks)
        index = SemanticSearchIndex()
        index.add(embeddings, chunks)

        top_chunks = retrieve_relevant_chunks(question, index)
        print("🔍 Top relevant chunks selected:", top_chunks[:2])

        answer = generate_answer_with_mistral(question, context_chunks=top_chunks)
        return jsonify({"answer": answer})
    
    except Exception as e:
        return jsonify({"error": f"Backend error: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting backend on http://localhost:5000")
    app.run(debug=True, port=5000)
