
AI-Powered Educational Platform where you can become a student of an AI operated school.
An adaptive learning system that personalizes educational content, quizzes, and study materials based on user performance. Integrates a Large Language Model (LLM) for question-answering and content recommendations, leveraging Meta’s Llama 2 (7B HF) as the core NLP engine.
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

1. Table of Contents
2. Project Overview
3. Key Features
4. Tech Stack & Tools
5. Project Structure
6. Installation & Setup
7. Usage
8. Seeding the Database
9. Taking a Quiz
10. Fetching Recommendations
11. Asking Questions (LLM)
12. Environment Variables
13. Notes on Llama 2 Usage
14. License
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
1. Project Overview
This platform provides an adaptive learning experience using AI-driven quizzes, personalized study resources, and a real-time dashboard. By analyzing user performance data, it recommends targeted materials to address individual learning gaps.
The system also features a chat-based question assistant powered by Llama 2, enabling students to ask topic-specific queries and receive detailed explanations.

2. Key Features
Adaptive Quizzes:
Users complete quizzes, and their performance is recorded to gauge strengths/weaknesses.

Personalized Recommendations:
An AI-based recommendation engine leverages stored user progress data to suggest relevant study materials.

LLM Question-Answering:
A question assistant (chat interface) integrates Llama 2 to handle user queries and provide explanations.

Real-Time Analytics:
Dashboards for users/instructors to track quiz performance, visualize correctness, and identify learning trends.

Modular Architecture:
Clean separation of backend (Python) and frontend (React) services, facilitating scalability and maintainability.
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
3. Tech Stack & Tools
Languages & Frameworks

Backend: [Python], [FastAPI or Flask], [MongoDB] for data storage
Frontend: [React], [TypeScript] for a dynamic user interface
LLM: Meta Llama 2 (7B HF) for NLP/Q&A
Other Tools

Hugging Face for LLM Inference API
Chart.js or similar for analytics dashboards
TailwindCSS for responsive design (if applicable)
VS Code as the primary IDE (with debugging extensions)
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
4. Project Structure
└── ...
backend/app/main.py – Entry point for the Python backend.
backend/app/routes/*.py – Contains API endpoints for quiz evaluation, recommendations, chat, etc.
backend/app/models/*.py – Core logic for AI-based recommendations, DB interactions, and QA pipeline.
frontend/src/* – React/TypeScript code for UI, including quiz forms, dashboards, and chat assistant.

____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
5. Installation & Setup
Clone the Repository
cd AI-Edu-Platform

Backend Setup
cd backend
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
Create a .env file (see Environment Variables below).

Frontend Setup
cd ../frontend
npm install
Adjust .env or configuration if needed for the frontend (e.g., REACT_APP_API_URL).

Run the Backend
# from the backend/ directory
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Open a browser at http://127.0.0.1:8000/docs to see the interactive API docs (Swagger UI).

Run the Frontend
# from the frontend/ directory
npm start
By default, it starts at http://localhost:3000.
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

6. Usage
6.1 Seeding the Database
(Optional step, if you want sample resources for recommendations.)

POST to http://127.0.0.1:8000/api/seed-resources/ using browser, Postman, or Swagger UI.
This inserts example resources (e.g. “Algebra Basics,” “Calculus 101”) into the Resources collection.

6.2 Taking a Quiz
Navigate to http://localhost:3000/quiz.
Enter a user ID (e.g., user123) and answer the quiz questions.
The system records your results and updates your progress in MongoDB.

6.3 Fetching Recommendations
Go to http://localhost:3000/learning-path.
Enter the same user ID used for the quiz.
Click Get Recommendations. If your score for a topic was below the threshold (e.g., <60), you’ll see relevant resources recommended for that topic.

6.4 Asking Questions (LLM)
Visit http://localhost:3000/chat.
Type in a question or statement. The AI chatbot, powered by Llama 2, will respond.
Each new user message re-sends the entire conversation to the backend endpoint (/api/chat/), which calls the Hugging Face Inference API for Llama 2.

____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

7. Environment Variables
In backend/.env, define:
MONGO_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/AdaptiveLearning"
HUGGINGFACE_TOKEN="hf_XXXXXXXXXXXX"
MONGO_URI: Connection string for your MongoDB (Atlas or local).
HUGGINGFACE_TOKEN: Your personal access token from Hugging Face.
Required to call Llama 2 (and other HF models) via the Inference API.
(Optional) MODEL_ID="meta-llama/Llama-2-7b-hf" if your code references an environment variable for the model ID.
You may also have a frontend .env for environment-specific settings (like REACT_APP_API_URL).

____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

8. Notes on Llama 2 Usage
License Acceptance: Llama 2 typically requires accepting the license on Hugging Face.
API Access: The free Inference API might block large models (403 errors). If so, either:
Use a smaller variant, or
Sign up for a paid Inference Endpoint on Hugging Face, or
Host the model locally on GPU (requires setup).
Rate Limits & Performance: The free tier can be slow or limited. For production usage, consider a self-hosted or paid solution.

____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

10. License
MIT License - open-source license.

Disclaimer: This project is for educational demonstration. The Llama 2 model usage is subject to Meta’s license terms and may not be used for commercial purposes without prior permission.

Enjoy exploring the AI-Powered Educational Platform! Feel free to raise issues or contribute via pull requests. If you have any questions, contact: [RoLBester]

____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
