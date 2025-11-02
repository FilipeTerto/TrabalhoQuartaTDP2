from fastapi import FastAPI
from controller.user_controller import router as user_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(user_router)

#monta os estaticos em view 
app.mount("/static", StaticFiles(directory="view"), name="static")
