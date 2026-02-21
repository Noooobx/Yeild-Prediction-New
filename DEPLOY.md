# Deployment Guide: Smart Crop Yield Prediction System

This guide outlines how to host your Data-Driven ML Application for free/cheap using popular cloud platforms.

## Architecture Overview

- **Frontend (React)**: Hosted on **Vercel** or **Netlify**.
- **Backend (Flask + ML Model)**: Hosted on **Render**, **Railway**, or **PythonAnywhere**.
- **Database**: No external DB required (Model is loaded from file).

---

## Part 1: Prepare Backend for Deployment

### 1. Create a `Procfile` (For Render/Railway)

In the `backend/` directory, create a file named `Procfile` (no extension):

```text
web: gunicorn app:app
```

### 2. Update `requirements.txt`

Ensure `gunicorn` is added to your production requirements.

```bash
pip install gunicorn
pip freeze > requirements.txt
```

### 3. Configure CORS

In `backend/app.py`, ensure CORS allows your frontend URL (once you have it). For now, allow all:

```python
CORS(app, resources={r"/*": {"origins": "*"}})
```

### 4. Push to GitHub

Make sure your project is pushed to a GitHub repository.

---

## Part 2: Deploy Backend (Render.com)

1.  **Sign up** at [render.com](https://render.com).
2.  Click **"New +"** -> **"Web Service"**.
3.  Connect your GitHub repository.
4.  **Settings**:
    - **Root Directory**: `backend` (Important!)
    - **Runtime**: Python 3
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `gunicorn app:app`
5.  Click **"Create Web Service"**.
6.  **Copy the URL** provided by Render (e.g., `https://yield-prediction-api.onrender.com`).

---

## Part 3: Deploy Frontend (Vercel)

1.  **Update API URL**:
    In `frontend/src/App.jsx`, replace the localhost URL with your new Render Backend URL:

    ```javascript
    // const API_URL = 'http://127.0.0.1:5000/predict';
    const API_URL = "https://your-backend-name.onrender.com/predict";
    ```

    _Better practice: Use environment variables (`import.meta.env.VITE_API_URL`)._

2.  **Sign up** at [vercel.com](https://vercel.com).
3.  Click **"Add New..."** -> **"Project"**.
4.  Import your GitHub repository.
5.  **Settings**:
    - **Framework Preset**: Vite
    - **Root Directory**: `frontend`
6.  Click **"Deploy"**.

---

## Part 4: Verification

1.  Open your Vercel URL (e.g., `https://smart-farm-app.vercel.app`).
2.  Run a prediction.
3.  **Note on Cold Starts**: Free tier backends (Render) verify "sleep" after inactivity. The first request might take 30-50 seconds. This is normal for free hosting.

---

## Alternative: Docker Deployment (Optional)

If you prefer using Docker, create a `Dockerfile` in `backend/`:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```
