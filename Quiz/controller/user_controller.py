from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from repository.quiz_repository import db

router = APIRouter()
templates = Jinja2Templates(directory="view")

@router.get("/", response_class=HTMLResponse)
def form_home(request:Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/add_user")
def add_user(name: str = Form(...)):
    db.users.insert_one({"name": name})
    return RedirectResponse ("/quiz", status_code=303)