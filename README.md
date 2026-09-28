# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight FastAPI web application inspired by the supplied project documentation. It provides:

- Question answering (`/qa`)
- Beginner-friendly concept explanation (`/explain`)
- Three-question MCQ generation (`/quiz`)
- Educational summarization (`/summarize`)
- Personalized learning paths (`/learn/recommendations`)

The supplied document specifies FastAPI, a simple HTML/CSS frontend, Gemini for Q&A/quiz/summary/learning paths, and LaMini-Flan-T5 for explanations. The implementation keeps those modules but uses the current Google Gen AI Python SDK and a current stable Gemini model by default.

## 1. Prerequisites

- Python 3.10 or newer
- VS Code
- A Gemini API key

## 2. Setup in VS Code

Open this folder in VS Code. Then open **Terminal → New Terminal**.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and replace `your_api_key_here` with your real key.

If PowerShell blocks activation, you can run the venv's Python directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 3. Run

```powershell
python -m uvicorn main:app --reload
```

Open:

`http://127.0.0.1:8000`

Health check:

`http://127.0.0.1:8000/health`

## 4. Test the backend

In another terminal:

```powershell
python -m pytest -q
```

You can also test the health endpoint in a browser. The AI endpoints require a valid `GEMINI_API_KEY`.

## 5. API examples

### Q&A

```http
POST /qa
Content-Type: application/json

{"text":"What is photosynthesis?"}
```

### Explanation

```http
POST /explain
Content-Type: application/json

{"text":"Explain blockchain to a beginner."}
```

### Quiz

```http
POST /quiz
Content-Type: application/json

{"text":"Photosynthesis is the process by which green plants use light energy to make food."}
```

### Summary

```http
POST /summarize
Content-Type: application/json

{"text":"Long educational passage..."}
```

### Learning path

```http
POST /learn/recommendations
Content-Type: application/json

{"text":"SQL"}
```

## 6. Optional local LaMini explanation backend

The project includes the LaMini-Flan-T5-783M integration described in the original documentation as an optional backend. It is intentionally not installed by default because PyTorch/model downloads are much heavier than the cloud-only application.

To install it:

```powershell
pip install -r requirements-local.txt
```

Then set in `.env`:

```env
EXPLANATION_BACKEND=local
```

If the local model cannot load, EduGenie automatically falls back to Gemini for the explanation request.

## 7. Common Windows issue: port 8000 already in use

If you see `WinError 10048`, another process is already using port 8000. Either stop the existing Uvicorn process or run EduGenie on another port:

```powershell
python -m uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
└── tests/
    └── test_app.py
```

## Security notes

- Never put the Gemini API key in frontend JavaScript.
- Never commit `.env` to Git.
- API input is validated with Pydantic.
- The frontend renders ordinary model output as text, and quiz content is escaped before being inserted into HTML.
- AI output should still be checked by learners; generative models can make mistakes.
