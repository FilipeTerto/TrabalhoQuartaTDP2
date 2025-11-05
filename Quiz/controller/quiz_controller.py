from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from model.questions import Question
from patterns.question_factory import QuestionFactory
from repository.quiz_repository import db  # ✅ Usa a conexão existente
from bson import ObjectId

router = APIRouter()
templates = Jinja2Templates(directory="view")


@router.get("/quiz", response_class=HTMLResponse)
async def show_quiz(request: Request):
    # Buscar perguntas do banco
    questions_data = list(db.questions.find())

    questions = []
    for q in questions_data:
        # Converte _id e alternativas.id para string
        q_id_str = str(q["_id"])
        alternatives_str = [
            {"id": str(alt["id"]), "texto": alt["texto"]} for alt in q["alternatives"]
        ]

        question = Question(
            id=q_id_str,
            text=q["text"],
            alternatives=alternatives_str,
            correct_answer_id=q["correct_answer_id"]
        )
        questions.append(question)

    return templates.TemplateResponse(
        "quiz.html",
        {"request": request, "questions": questions}
    )


@router.post("/quiz", response_class=HTMLResponse)
async def submit_quiz(request: Request):
    form = await request.form()
    answers = dict(form)

    questions_data = list(db.questions.find())
    questions = []
    for q in questions_data:
        q_id_str = str(q["_id"])
        question = Question(
            id=q_id_str,
            text=q["text"],
            alternatives=[{"id": str(alt["id"]), "texto": alt["texto"]} for alt in q["alternatives"]],
            correct_answer_id=q["correct_answer_id"]
        )
        questions.append(question)

    score = 0
    for question in questions:
        user_answer = answers.get(str(question.id))
        if user_answer and int(user_answer) == question.correct_answer_id:
            score += 1

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "score": score,
            "total": len(questions),
        }
    )
