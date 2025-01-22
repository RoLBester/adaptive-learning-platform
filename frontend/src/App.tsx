// frontend/src/App.tsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar.tsx";
import Dashboard from "./components/Dashboard.tsx";
import LearningPath from "./components/LearningPath.tsx";
import QuestionAssistant from "./components/QuestionAssistant.tsx";
import QuizPage from "./components/QuizPage.tsx";
import ChatAssistant from "./components/ChatAssistant.tsx";

const HomePage: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] bg-gradient-to-b from-indigo-600 to-purple-600 text-white p-4 text-center rounded-lg shadow">
      <h1 className="text-4xl font-bold mb-4">
        Welcome to the Adaptive Learning Platform
      </h1>
      <p className="max-w-2xl text-lg mb-6">
        Explore quizzes, personalized recommendations, and chat with our AI –
        all in one interactive learning experience!
      </p>
      <div className="space-x-4">
        <a
          href="/quiz"
          className="bg-white text-indigo-700 font-semibold px-4 py-2 rounded shadow hover:bg-gray-100 transition duration-200"
        >
          Take a Quiz
        </a>
        <a
          href="/chat"
          className="bg-white text-purple-700 font-semibold px-4 py-2 rounded shadow hover:bg-gray-100 transition duration-200"
        >
          Chat with AI
        </a>
      </div>
    </div>
  );
};

const App: React.FC = () => {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-gray-100">
        <Navbar />
        <main className="flex-grow container mx-auto p-4">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/quiz" element={<QuizPage />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/learning-path" element={<LearningPath />} />
            <Route path="/question-assistant" element={<QuestionAssistant />} />
            <Route path="/chat" element={<ChatAssistant />} />
          </Routes>
        </main>
        <footer className="bg-gray-900 text-white text-center py-2">
          &copy; {new Date().getFullYear()} Adaptive Learning Platform
        </footer>
      </div>
    </Router>
  );
};

export default App;
