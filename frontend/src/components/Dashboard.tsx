// frontend/src/components/Dashboard.tsx
import React, { useEffect, useRef, useState } from "react";
import Chart from "chart.js/auto";
import apiClient from "../api/apiClient.ts";

const Dashboard: React.FC = () => {
  const [userId, setUserId] = useState("user123");
  const [performance, setPerformance] = useState<
    { index: number; question: string; isCorrect: boolean }[]
  >([]);
  const [error, setError] = useState("");
  const chartRef = useRef<Chart | null>(null);

  const fetchPerformance = async () => {
    setError("");
    try {
      const response = await apiClient.get(`/api/user-performance/${userId}`);
      // => { performance: [ {index, question, isCorrect}, ... ] }
      setPerformance(response.data.performance || []);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch performance data.");
    }
  };

  useEffect(() => {
    if (chartRef.current) {
      chartRef.current.destroy();
    }
    if (performance.length === 0) return;

    const canvas = document.getElementById("answersChart") as HTMLCanvasElement;
    const dataValues = performance.map((p) => (p.isCorrect ? 1 : 0));
    const labels = performance.map((p) => `Q${p.index}`);

    chartRef.current = new Chart(canvas, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Answer Correctness (1=Correct, 0=Wrong)",
            data: dataValues,
            backgroundColor: dataValues.map((val) =>
              val === 1 ? "rgba(75, 192, 192, 0.5)" : "rgba(255, 99, 132, 0.5)"
            ),
            borderColor: dataValues.map((val) =>
              val === 1 ? "rgba(75, 192, 192, 1)" : "rgba(255, 99, 132, 1)"
            ),
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            max: 1,
            ticks: {
              stepSize: 1,
            },
          },
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                const idx = context.dataIndex;
                const wasCorrect = dataValues[idx] === 1;
                return wasCorrect
                  ? `Correct! ${performance[idx].question}`
                  : `Wrong! ${performance[idx].question}`;
              },
            },
          },
        },
      },
    });
  }, [performance]);

  return (
    <div className="bg-white p-6 rounded-lg shadow text-gray-800 max-w-3xl mx-auto">
      <h2 className="text-2xl font-semibold mb-4">
        User Performance Dashboard
      </h2>
      <div className="mb-4">
        <label htmlFor="userId" className="block font-medium mb-1">
          User ID:
        </label>
        <input
          id="userId"
          type="text"
          className="border border-gray-300 rounded px-3 py-2 mr-2"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
        />
        <button
          onClick={fetchPerformance}
          className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 transition"
        >
          Fetch Performance
        </button>
      </div>

      {error && <p className="text-red-600">{error}</p>}
      {performance.length > 0 ? (
        <div className="mt-4">
          <canvas id="answersChart" />
        </div>
      ) : (
        <p className="text-gray-600 mt-4">
          No performance data yet. Please take a quiz first!
        </p>
      )}
    </div>
  );
};

export default Dashboard;
