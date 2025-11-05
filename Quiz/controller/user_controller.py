from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from repository.quiz_repository import db
from bson import ObjectId

router = APIRouter()
templates = Jinja2Templates(directory="view")

@router.get("/", response_class=HTMLResponse)
def form_home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/add_user")
def add_user(name: str = Form(...)):
    # Insere o usuário no MongoDB
    result = db.users.insert_one({"name": name})
    user_id = str(result.inserted_id)  # Pega o _id gerado e converte para string

    # Redireciona para o quiz passando o user_id como query param
    return RedirectResponse(f"/quiz?user_id={user_id}", status_code=303)
