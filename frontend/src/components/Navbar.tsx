// frontend/src/components/Navbar.tsx
import React from "react";
import { Link } from "react-router-dom";

const Navbar: React.FC = () => {
  return (
    <header className="bg-gray-900 text-white shadow">
      <nav className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="font-bold text-xl">Adaptive Learning Platform</div>
        <div className="space-x-4">
          <Link
            to="/"
            className="hover:bg-gray-700 px-3 py-2 rounded transition duration-200"
          >
            Home
          </Link>
          <Link
            to="/quiz"
            className="hover:bg-gray-700 px-3 py-2 rounded transition duration-200"
          >
            Quiz
          </Link>
          <Link
            to="/dashboard"
            className="hover:bg-gray-700 px-3 py-2 rounded transition duration-200"
          >
            Dashboard
          </Link>
          <Link
            to="/learning-path"
            className="hover:bg-gray-700 px-3 py-2 rounded transition duration-200"
          >
            Learning Path
          </Link>
          <Link
            to="/chat"
            className="hover:bg-gray-700 px-3 py-2 rounded transition duration-200"
          >
            Chat AI
          </Link>
        </div>
      </nav>
    </header>
  );
};

export default Navbar;
