import React, { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import apiClient from "./api/apiClient.ts"; // Ensure this path matches the actual location of apiClient.ts

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const App = () => {
  const [chartData, setChartData] = useState({
    labels: [], // Placeholder for labels
    datasets: [], // Placeholder for datasets
  });

  useEffect(() => {
    // Fetch data from the backend
    apiClient
      .get("/sales")
      .then((response) => {
        const { labels, data } = response.data;

        // Debugging: Log the fetched data
        console.log("Fetched Data:", labels, data);

        // Update chart data state
        setChartData({
          labels,
          datasets: [
            {
              label: "Monthly Sales",
              data,
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 1,
            },
          ],
        });
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  // Chart options
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: "Monthly Sales Data (Dynamic)",
      },
    },
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-r from-blue-400 to-purple-500 text-white">
      <header className="mb-8 text-center">
        <h1 className="text-4xl font-bold mb-2">Welcome to the Dashboard</h1>
        <p className="text-lg">Visualizing Monthly Sales Data</p>
      </header>
      <main className="w-11/12 max-w-4xl bg-white p-6 rounded-lg shadow-lg text-black">
        {/* Render the chart */}
        {chartData.labels.length > 0 ? (
          <Bar data={chartData} options={options} />
        ) : (
          <p className="text-center text-gray-500">Loading data...</p>
        )}
      </main>
    </div>
  );
};

export default App;
