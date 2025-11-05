from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from repository.quiz_repository import db
from bson import ObjectId

router = APIRouter()
templates = Jinja2Templates(directory="view")

@router.post("/quiz/submit", response_class=HTMLResponse)
async def submit_quiz(request: Request):
    form = await request.form()
    answers = dict(form)

    # Aqui, só um exemplo de user_id fixo
    user_id = "6900aefe1b83af9368dd1c15"

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
