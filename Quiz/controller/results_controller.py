from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from repository.quiz_repository import db
from bson import ObjectId

router = APIRouter()
templates = Jinja2Templates(directory="view")


@router.get("/results", response_class=HTMLResponse)
async def show_results(request: Request, user_id: str):
    """
    Mostra os resultados do quiz do usuário e o ranking completo.
    """
    # Busca resultados do usuário
    user_result = db.results.find_one({"users_id": user_id})
    
    if not user_result:
        return HTMLResponse("Nenhum resultado encontrado para este usuário.", status_code=404)
    
    # Busca o ranking completo ordenado por total_score decrescente
    ranking_cursor = db.ranking.find().sort("total_score", -1)
    ranking_list = list(ranking_cursor)

    # Adiciona posição no ranking
    for index, user in enumerate(ranking_list, start=1):
        user["rank_position"] = index

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "user_result": user_result,
            "ranking": ranking_list
        }
    )
