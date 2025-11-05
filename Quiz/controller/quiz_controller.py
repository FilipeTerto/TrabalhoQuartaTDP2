from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from repository.quiz_repository import db
from model.questions import Question
from bson import ObjectId

router = APIRouter()
templates = Jinja2Templates(directory="view")


@router.get("/quiz", response_class=HTMLResponse)
async def show_quiz(request: Request, user_id: str):
    """
    Mostra as perguntas do quiz para o usuário identificado por user_id.
    """
    questions_data = list(db.questions.find())

    questions = []
    for q in questions_data:
        q["_id"] = str(q["_id"])  # converte ObjectId para string
        for alt in q["alternatives"]:
            alt["id"] = str(alt["id"])  # converte id de alternativa para string
            alt["text"] = alt.pop("texto")  # transforma "texto" do Mongo em "text"
        questions.append(Question(**q))

    return templates.TemplateResponse(
        "quiz.html",
        {
            "request": request,
            "questions": questions,
            "user_id": user_id  # passado para o hidden input do form
        }
    )


@router.post("/quiz/submit", response_class=HTMLResponse)
async def submit_quiz(request: Request):
    """
    Recebe as respostas do quiz, salva no banco, calcula score e atualiza ranking.
    """
    form = await request.form()
    answers = dict(form)

    user_id = answers.get("user_id")  # pega do hidden input
    if not user_id:
        return HTMLResponse("Erro: user_id não fornecido", status_code=400)

    questions_data = list(db.questions.find())
    score = 0

    for q in questions_data:
        qid_str = str(q["_id"])
        if qid_str in answers:
            selected = int(answers[qid_str])
            correct = q["correct_answer_id"]
            is_correct = selected == correct
            if is_correct:
                score += 1

            db.answers.insert_one({
                "users_id": user_id,
                "questions_id": qid_str,
                "is_correct": is_correct
            })

    total_questions = len(questions_data)
    percentage = int(score / total_questions * 100)

    db.results.insert_one({
        "users_id": user_id,
        "total_score": score,
        "total_questions": total_questions,
        "correct_answers": score,
        "percentage": percentage
    })

    # Atualiza ranking
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    db.ranking.update_one(
        {"users_id": user_id},
        {"$set": {"username": user_data["name"], "total_score": score}},
        upsert=True
    )

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "score": score,
            "total": total_questions,
            "percentage": percentage
        }
    )
