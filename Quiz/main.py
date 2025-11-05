from fastapi import FastAPI
from controller.quiz_controller import router as quiz_router
from controller.user_controller import router as user_router
from controller.submit_controller import router as submit_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(submit_router)
app.include_router(quiz_router)
app.include_router(user_router)

app.mount("/static", StaticFiles(directory="view"), name="static")
