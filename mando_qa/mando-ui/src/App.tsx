import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setAnswer("");
    setError("");

    if (!file || !question.trim()) {
      setError("Please provide both a file and a question.");
      setLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("question", question);

    const BACKEND_URL = "http://localhost:5000/ask";
    console.log("📡 Sending request to:", BACKEND_URL);

    try {
      const response = await fetch(BACKEND_URL, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log("📬 Response from backend:", data);

      if (data.answer) {
        setAnswer(data.answer);
      } else {
        setError(data.error || "Unexpected error from backend.");
      }
    } catch (err) {
      console.error("❌ Request error:", err);
      setError("Failed to reach the backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-8">
      <h1 className="text-3xl font-bold mb-6">🧠 Mando QA</h1>

      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded shadow-md w-full max-w-xl space-y-4"
      >
        <input
          type="file"
          accept=".pdf,.docx,.txt,.csv,.pptx,.xlsx,.json,.png,.jpeg,.jpg"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="w-full"
        />

        <textarea
          placeholder="Ask your question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded"
          rows={3}
        />

        <button
          type="submit"
          className="bg-black text-white px-4 py-2 rounded hover:bg-gray-800 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Processing..." : "Ask"}
        </button>
      </form>

      {answer && (
        <div className="mt-6 p-4 bg-green-100 rounded w-full max-w-xl">
          <strong>Answer:</strong>
          <p>{answer}</p>
        </div>
      )}

      {error && (
        <div className="mt-6 p-4 bg-red-100 text-red-800 rounded w-full max-w-xl">
          {error}
        </div>
      )}
    </div>
  );
}

export default App;
