// frontend/src/components/LearningPath.tsx
import React, { useState, useEffect } from "react";
import apiClient from "../api/apiClient.ts";
import { RECOMMENDATIONS_ENDPOINT, RAG_RECOMMEND_ENDPOINT, VECTOR_STATS_ENDPOINT } from "../api/endpoints.ts";

interface RecommendedResource {
  title?: string;
  url?: string;
  topic?: string;
  difficulty?: string;
  reason?: string;
  description?: string;
  similarity_score?: number;
  relevance?: string;
}

const LearningPath: React.FC = () => {
  const [userId, setUserId] = useState("user123");
  const [recommendations, setRecommendations] = useState<
    (RecommendedResource | string)[]
  >([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [useRAG, setUseRAG] = useState(true);
  const [ragMessage, setRagMessage] = useState("");
  const [vectorStats, setVectorStats] = useState<any>(null);

  // Check vector database status on mount
  useEffect(() => {
    const checkVectorStats = async () => {
      try {
        const response = await apiClient.get(VECTOR_STATS_ENDPOINT);
        setVectorStats(response.data);
      } catch (err) {
        console.error("Failed to fetch vector stats:", err);
      }
    };
    checkVectorStats();
  }, []);

  const fetchRecommendations = async () => {
    setLoading(true);
    setError("");
    setRecommendations([]);
    setRagMessage("");

    try {
      if (useRAG) {
        // Use RAG endpoint
        const response = await apiClient.post(RAG_RECOMMEND_ENDPOINT, {
          user_id: userId,
          n_results: 5,
          min_similarity: 0.5
        });

        setRecommendations(response.data.recommendations || []);
        setRagMessage(response.data.message || "");
      } else {
        // Use baseline endpoint
        const response = await apiClient.post(RECOMMENDATIONS_ENDPOINT, {
          user_id: userId,
          user_data: {},
        });
        setRecommendations(response.data.recommendations || []);
      }
    } catch (err) {
      console.error(err);
      setError("Failed to fetch recommendations.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow text-gray-800 max-w-4xl mx-auto">
      <h2 className="text-2xl font-semibold mb-4">
        Personalized Learning Path
        {useRAG && <span className="text-sm text-green-600 ml-2">✨ RAG-Enhanced</span>}
      </h2>

      {/* Vector Database Status */}
      {vectorStats && (
        <div className={`mb-4 p-3 rounded-lg text-sm ${
          vectorStats.status === 'ready'
            ? 'bg-green-50 text-green-800 border border-green-200'
            : 'bg-yellow-50 text-yellow-800 border border-yellow-200'
        }`}>
          <strong>Vector DB Status:</strong> {vectorStats.message}
          {vectorStats.status === 'empty' && (
            <span className="ml-2 text-red-600">
              (Please run /api/embed-resources/ first!)
            </span>
          )}
        </div>
      )}

      {/* User ID Input and RAG Toggle */}
      <div className="mb-4">
        <label className="block font-medium mb-1" htmlFor="userId">
          User ID:
        </label>
        <input
          id="userId"
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          className="border border-gray-300 rounded px-3 py-2 w-full mb-3"
        />

        {/* RAG Toggle Switch */}
        <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg mb-3">
          <label className="flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={useRAG}
              onChange={(e) => setUseRAG(e.target.checked)}
              className="mr-2 h-5 w-5"
            />
            <span className="font-medium">
              Use RAG (Semantic Search)
            </span>
          </label>
          {vectorStats && vectorStats.status === 'ready' && (
            <span className="text-sm text-green-600">✓ {vectorStats.collection_size} resources embedded</span>
          )}
          {vectorStats && vectorStats.status === 'empty' && (
            <span className="text-sm text-red-600">⚠️ No embeddings found</span>
          )}
        </div>

        <button
          onClick={fetchRecommendations}
          disabled={loading}
          className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 transition disabled:bg-gray-400 w-full"
        >
          {loading ? "Loading..." : "Get Recommendations"}
        </button>
      </div>

      {/* RAG Message */}
      {ragMessage && (
        <div className="mb-4 p-3 bg-blue-100 text-blue-800 rounded">
          <p className="text-sm">{ragMessage}</p>
        </div>
      )}

      {loading && <p className="text-blue-600">Loading recommendations...</p>}
      {error && <p className="text-red-600">{error}</p>}

      {/* Render array of either resource objects or fallback strings */}
      {recommendations.length > 0 && (
        <ul className="space-y-4 mt-4">
          {recommendations.map((rec, i) => {
            // If 'rec' is a string fallback
            if (typeof rec === "string") {
              return (
                <li key={i} className="text-gray-600">
                  {rec}
                </li>
              );
            }

            // Otherwise it's a resource object
            return (
              <li key={i} className="border-b border-gray-200 pb-4">
                <div className="flex justify-between items-start">
                  <h3 className="font-medium text-lg">
                    {rec.title}
                  </h3>
                  {rec.similarity_score !== undefined && (
                    <span className={`text-xs px-2 py-1 rounded ${
                      rec.similarity_score >= 0.8 ? 'bg-green-100 text-green-800' :
                      rec.similarity_score >= 0.6 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {rec.relevance || `${(rec.similarity_score * 100).toFixed(0)}% match`}
                    </span>
                  )}
                </div>

                <p className="text-sm text-gray-500 mt-1">
                  {rec.topic && `Topic: ${rec.topic}`}
                  {rec.topic && rec.difficulty && " • "}
                  {rec.difficulty && `Level: ${rec.difficulty}`}
                </p>

                {rec.description && (
                  <p className="text-sm text-gray-600 mt-2">{rec.description}</p>
                )}

                {rec.url && (
                  <a
                    href={rec.url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-blue-500 underline hover:text-blue-700 text-sm mt-2 inline-block"
                  >
                    View Resource →
                  </a>
                )}

                {rec.reason && (
                  <p className="text-sm text-gray-600 mt-1">
                    <strong>Why recommended?</strong> {rec.reason}
                  </p>
                )}
              </li>
            );
          })}
        </ul>
      )}

      {!loading && !error && recommendations.length === 0 && !ragMessage && (
        <p className="text-gray-600">
          No recommendations yet. Please take a quiz first.
        </p>
      )}
    </div>
  );
};

export default LearningPath;
