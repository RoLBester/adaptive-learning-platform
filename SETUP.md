# Quick Setup Guide

## Prerequisites
- Python 3.12+
- Node.js 18+
- MongoDB Atlas account (or local MongoDB)
- Hugging Face account

## Environment Setup

### 1. Create Backend Environment File
```bash
cd backend
cp .env.example .env
```

Then edit `backend/.env` with your credentials:
```env
MONGO_URI=mongodb+srv://your_username:your_password@your_cluster.mongodb.net/AdaptiveLearning?retryWrites=true&w=majority
HUGGINGFACE_TOKEN=hf_YourActualTokenHere
```

### 2. Install Backend Dependencies
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r ../requirements.txt
```

### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
```

## Running the Application

### Terminal 1 - Backend Server
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```
API docs available at: http://127.0.0.1:8000/docs

### Terminal 2 - Frontend Development Server
```bash
cd frontend
npm start
```
Opens at: http://localhost:3000

## Database Setup

### Seed Sample Data (First Time Only)
1. Go to http://127.0.0.1:8000/docs
2. Find `/api/seed-resources/` endpoint
3. Click "Try it out" → "Execute"

This populates study materials for the recommendation engine.

## Testing the Features

1. **Take a Quiz**: Go to http://localhost:3000/quiz
2. **View Performance**: Go to http://localhost:3000/dashboard
3. **Get Recommendations**: Go to http://localhost:3000/learning-path
4. **Chat with AI**: Go to http://localhost:3000/chat

## Troubleshooting

- **MongoDB connection fails**: Check your IP is whitelisted in MongoDB Atlas → Network Access
- **Chat is slow/fails**: Free Hugging Face API has rate limits. Wait 30-60 seconds between requests.
- **Port 8000 already in use**: Kill existing process with `lsof -ti:8000 | xargs kill -9`
