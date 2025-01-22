import React, { useState } from "react";
import apiClient from "../api/apiClient.ts";
import { QUESTIONS_ENDPOINT } from "../api/endpoints.ts";

const QuestionAssistant = () => {
  const [question, setQuestion] = useState("");
  const [context, setContext] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setAnswer("");
    setError("");

    try {
      const response = await apiClient.post(QUESTIONS_ENDPOINT, {
        question,
        context,
      });
      setAnswer(response.data.answer);
    } catch (err) {
      console.error("Error:", err);
      setError("Failed to get an answer. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-4">
      <h2 className="text-2xl font-bold text-center mb-4">
        AI Question Assistant
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="question" className="block text-sm font-medium">
            Your Question:
          </label>
          <input
            type="text"
            id="question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>
        <div>
          <label htmlFor="context" className="block text-sm font-medium">
            Context:
          </label>
          <textarea
            id="context"
            value={context}
            onChange={(e) => setContext(e.target.value)}
            className="w-full border rounded px-3 py-2"
            rows={4}
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
          disabled={loading}
        >
          {loading ? "Getting Answer..." : "Submit"}
        </button>
      </form>
      {answer && (
        <div className="mt-4 p-4 bg-green-100 rounded">
          <p className="text-lg font-medium">Answer:</p>
          <p>{answer}</p>
        </div>
      )}
      {!answer && !loading && (
        <div className="mt-4 p-4 bg-yellow-100 rounded">
          <p className="text-lg font-medium">Note:</p>
          <p>
            The AI couldn't generate a precise answer. Try rephrasing your
            question or providing more context.
          </p>
        </div>
      )}
    </div>
  );
};

export default QuestionAssistant;
