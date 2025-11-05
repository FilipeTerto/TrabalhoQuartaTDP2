from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from repository.quiz_repository import db
from bson import ObjectId

router = APIRouter()
templates = Jinja2Templates(directory="view")


@router.post("/quiz/submit", response_class=HTMLResponse)
async def submit_quiz(request: Request):
    """
    Recebe as respostas do quiz, salva no banco, calcula score,
    atualiza ranking e exibe os resultados.
    """
    form = await request.form()
    answers = dict(form)

    # Pega user_id do hidden input enviado pelo formulário
    user_id = answers.get("user_id")
    if not user_id:
        return HTMLResponse("Erro: user_id não fornecido", status_code=400)

    # Buscar todas as perguntas do banco
    questions_data = list(db.questions.find())
    score = 0

    # Processa cada resposta
    for q in questions_data:
        qid_str = str(q["_id"])
        if qid_str in answers:
            selected = int(answers[qid_str])
            correct = q["correct_answer_id"]
            is_correct = selected == correct
            if is_correct:
                score += 1

            # Salva a resposta do usuário
            db.answers.insert_one({
                "users_id": user_id,
                "questions_id": qid_str,
                "is_correct": is_correct
            })

    total_questions = len(questions_data)
    percentage = int(score / total_questions * 100)

    # Salva resultado final do usuário
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

    # Buscar ranking completo
    ranking_list = list(db.ranking.find().sort("total_score", -1))

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "user_result": {
                "users_id": user_id,
                "total_questions": total_questions,
                "correct_answers": score,
                "total_score": score,
                "percentage": percentage
            },
            "ranking": ranking_list
        }
    )
