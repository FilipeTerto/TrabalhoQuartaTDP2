from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from model.questions import Question
from patterns.question_factory import QuestionFactory
from patterns.bonus_question_decorator import BonusQuestion
from repository.quiz_repository import db  # conexão existente

router = APIRouter()
templates = Jinja2Templates(directory="view")

@router.get("/bonus_quiz", response_class=HTMLResponse)
async def show_bonus_quiz(request: Request):
    questions_data = list(db.questions.find())
    factory = QuestionFactory()
    questions = []

    for q_data in questions_data:
        q = factory.create_question(
            text=q_data["text"],
            alternatives=q_data["alternatives"],
            correct_answer_id=q_data["correct_answer_id"]
        )
        # Exemplo: perguntas com correct_answer_id == 1 são bônus
        if q.correct_answer_id == 1:
            q = BonusQuestion(q)
        questions.append(q)

    return templates.TemplateResponse(
        "quiz.html",
        {"request": request, "questions": questions}
    )

@router.post("/bonus_quiz", response_class=HTMLResponse)
async def submit_bonus_quiz(request: Request):
    form = await request.form()
    answers = dict(form)

    questions_data = list(db.questions.find())
    factory = QuestionFactory()
    questions = []

    for q_data in questions_data:
        q = factory.create_question(
            text=q_data["text"],
            alternatives=q_data["alternatives"],
            correct_answer_id=q_data["correct_answer_id"]
        )
        if q.correct_answer_id == 1:
            q = BonusQuestion(q)
        questions.append(q)

    score = 0
    for q in questions:
        user_answer = int(answers.get(str(q.id), -1))
        if user_answer == q.correct_answer_id:
            score += q.score_multiplier() if hasattr(q, "score_multiplier") else 1

    return templates.TemplateResponse(
        "result.html",
        {"request": request, "score": score, "total": len(questions)}
    )
