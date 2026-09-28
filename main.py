from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="EduGenie", version="1.0.0", description="Google Gemini powered learning assistant")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


@app.exception_handler(Exception)
async def handle_application_error(request: Request, exc: Exception):
    if isinstance(exc, ValueError):
        status_code = 400
    else:
        status_code = 500
    return JSONResponse(status_code=status_code, content={"detail": str(exc)})

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: TextRequest):
    return {"result": answer_question(payload.text)}


@app.post("/explain")
async def explain(payload: TextRequest):
    return {"result": explain_topic(payload.text)}


@app.post("/quiz")
async def quiz(payload: TextRequest):
    return {"result": generate_quiz(payload.text)}


@app.post("/summarize")
async def summarize(payload: TextRequest):
    return {"result": summarize_text(payload.text)}


@app.post("/learn/recommendations")
async def learning_recommendations(payload: TextRequest):
    return {"result": get_learning_recommendations(payload.text)}
