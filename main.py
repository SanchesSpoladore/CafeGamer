from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="models/static"), name="static")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("inicio/index.html", {"request": request})

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login/index.html", {"request": request})

@app.get("/jogo/SpaceInvaders")
async def SpaceInvaders(request: Request):
    return templates.TemplateResponse("jogo/SpaceInvaders/index.html", {"request": request})

@app.get("/jogo/PacMan")
async def PacMan(request: Request):
    return templates.TemplateResponse("jogo/Pac-Man/index.html", {"request": request})

@app.get("/jogo/PacMan/menu")
async def SpaceInvadersMenu(request: Request):
    return templates.TemplateResponse("jogo/Pac-Man/menu.html", {"request": request})

@app.get("/jogo/batalhanaval")
async def batalhanaval(request: Request):
    return templates.TemplateResponse("jogo/batalhanaval/index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
