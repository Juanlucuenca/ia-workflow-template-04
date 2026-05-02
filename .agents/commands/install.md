---
description: Install dependencies and start the dev server
---

# Install

## Run

Think through each step carefully to ensure nothing is missed.

### Backend Setup

1. Navigate to backend: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Start dev server: `uvicorn app.main:app --reload`
4. Verify API running at http://localhost:8000/health

### Frontend Setup

1. Navigate to frontend: `cd frontend`
2. Install dependencies: `npm install`
3. Start dev server: `npm run dev`
4. Verify app running at http://localhost:5173

Both servers must run concurrently (separate terminals).

## Report

Output what you've done in a concise bullet point list:
- Backend deps: installed or already up to date
- Frontend deps: installed or already up to date
- Backend server: http://localhost:8000
- Frontend server: http://localhost:5173
- Any issues encountered
