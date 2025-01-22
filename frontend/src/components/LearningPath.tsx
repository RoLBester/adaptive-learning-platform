// frontend/src/components/LearningPath.tsx
import React, { useState } from "react";
import apiClient from "../api/apiClient.ts";
import { RECOMMENDATIONS_ENDPOINT } from "../api/endpoints.ts";

interface RecommendedResource {
  title?: string;
  url?: string;
  topic?: string;
  difficulty?: string;
  reason?: string;
}

const LearningPath: React.FC = () => {
  const [userId, setUserId] = useState("user123");
  const [recommendations, setRecommendations] = useState<
    (RecommendedResource | string)[]
  >([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchRecommendations = async () => {
    setLoading(true);
    setError("");
    setRecommendations([]);
    try {
      const response = await apiClient.post(RECOMMENDATIONS_ENDPOINT, {
        user_id: userId,
        user_data: {},
      });
      // Could return an array of resource objects OR strings if fallback
      setRecommendations(response.data.recommendations || []);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch recommendations.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow text-gray-800 max-w-3xl mx-auto">
      <h2 className="text-2xl font-semibold mb-4">
        Personalized Learning Path
      </h2>
      <div className="mb-4">
        <label className="block font-medium mb-1" htmlFor="userId">
          User ID:
        </label>
        <input
          id="userId"
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          className="border border-gray-300 rounded px-3 py-2 mr-2"
        />
        <button
          onClick={fetchRecommendations}
          className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 transition"
        >
          Get Recommendations
        </button>
      </div>

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
                <h3 className="font-medium text-lg">
                  {rec.title}{" "}
                  {rec.topic && rec.difficulty && (
                    <span className="text-sm text-gray-500">
                      (Topic: {rec.topic}, {rec.difficulty})
                    </span>
                  )}
                </h3>
                {rec.url && (
                  <a
                    href={rec.url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-blue-500 underline hover:text-blue-700"
                  >
                    {rec.url}
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

      {!loading && !error && recommendations.length === 0 && (
        <p className="text-gray-600">
          No recommendations yet. Please take a quiz.
        </p>
      )}
    </div>
  );
};

export default LearningPath;
