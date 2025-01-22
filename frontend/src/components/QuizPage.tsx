// frontend/src/components/QuizPage.tsx
import React, { useState } from "react";
import apiClient from "../api/apiClient.ts";
import { QUIZ_EVALUATION_ENDPOINT } from "../api/endpoints.ts";

const QuizPage: React.FC = () => {
  const [userId, setUserId] = useState("user123");
  const [submitted, setSubmitted] = useState(false);

  const questions = [
    {
      id: "q1",
      topic: "Algebra",
      text: "Solve for x: 2x + 5 = 15",
      options: ["x = 3", "x = 5", "x = 10", "x = 20"],
      correct: "x = 5",
    },
    {
      id: "q2",
      topic: "Algebra",
      text: "Which of the following expressions is equivalent to (x+2)(x+3)?",
      options: ["x² + 5x + 6", "x² + 6", "x² + 6x + 5", "x² + 2x + 3x"],
      correct: "x² + 5x + 6",
    },
    {
      id: "q3",
      topic: "Geometry",
      text: "The sum of the interior angles of a triangle is:",
      options: ["90°", "180°", "270°", "360°"],
      correct: "180°",
    },
    {
      id: "q4",
      topic: "Calculus",
      text: "What is the derivative of x²?",
      options: ["1", "2x", "x", "x²/2"],
      correct: "2x",
    },
  ];

  const [answers, setAnswers] = useState<Record<string, string>>({});

  const handleAnswerChange = (qId: string, choice: string) => {
    setAnswers({ ...answers, [qId]: choice });
  };

  const handleSubmitQuiz = async () => {
    let totalCorrect = 0;
    const quizData = questions.map((q) => {
      const userAnswer = answers[q.id];
      const isCorrect = userAnswer === q.correct;
      if (isCorrect) totalCorrect++;
      return {
        question: q.text,
        topic: q.topic,
        userAnswer,
        correctAnswer: q.correct,
        isCorrect,
      };
    });

    const score = totalCorrect * 25; // 4 questions => max 100

    try {
      const response = await apiClient.post(QUIZ_EVALUATION_ENDPOINT, {
        user_id: userId,
        quiz_data: { questions: quizData },
        score,
        topic: "Mixed",
      });
      console.log("Quiz submission:", response.data);
      setSubmitted(true);
      alert(`Quiz submitted! You scored ${score} points.`);
    } catch (err) {
      console.error("Error submitting quiz:", err);
      alert("Failed to submit quiz!");
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow text-gray-800 max-w-2xl mx-auto">
      <h2 className="text-2xl font-semibold mb-6">Take a Quiz</h2>
      {!submitted && (
        <>
          <div className="mb-4">
            <label htmlFor="userId" className="block font-medium mb-1">
              User ID:
            </label>
            <input
              id="userId"
              type="text"
              className="border border-gray-300 rounded px-3 py-2 w-64"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
            />
          </div>
          {questions.map((q) => (
            <div key={q.id} className="mb-4">
              <p className="font-medium mb-1">
                {q.text} <span className="italic text-sm">({q.topic})</span>
              </p>
              <div className="flex flex-col space-y-1 pl-4">
                {q.options.map((opt) => (
                  <label key={opt} className="flex items-center space-x-2">
                    <input
                      type="radio"
                      name={q.id}
                      value={opt}
                      checked={answers[q.id] === opt}
                      onChange={() => handleAnswerChange(q.id, opt)}
                    />
                    <span>{opt}</span>
                  </label>
                ))}
              </div>
            </div>
          ))}
          <button
            className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 transition duration-200"
            onClick={handleSubmitQuiz}
          >
            Submit Quiz
          </button>
        </>
      )}

      {submitted && (
        <div className="text-green-700 font-medium">
          Quiz submitted! Go to{" "}
          <a href="/learning-path" className="underline text-blue-600">
            Learning Path
          </a>{" "}
          for recommendations.
        </div>
      )}
    </div>
  );
};

export default QuizPage;
