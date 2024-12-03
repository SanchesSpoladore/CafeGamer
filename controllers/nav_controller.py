from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from routes.api_routes import router as api_routes
from routes.game_routes import router as game_routes
from routes.public_routes import router as public_routes
from routes.private_routes import router as private_routes
import uvicorn

from utils.auth import checar_autenticacao, checar_autorizacao 

load_dotenv()
app = FastAPI()
#app = FastAPI(dependencies=[Depends(checar_autorizacao)])

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/template/jogos", StaticFiles(directory="templates/jogos"), name="jogos")
app.middleware("http")(checar_autenticacao)

# ============== Include das rotas

app.include_router(public_routes)
app.include_router(private_routes, dependencies=[Depends(checar_autorizacao)])
app.include_router(game_routes, dependencies=[Depends(checar_autorizacao)])
app.include_router(api_routes, dependencies=[Depends(checar_autorizacao)])



#region ERRO

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("error.html", {"request": request}, status_code=404)
    return HTMLResponse(content=str(exc.detail), status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return templates.TemplateResponse("error.html", {"request": request, "message": "Dados inválidos enviados!"}, status_code=400)

#endregion ERRO

# ============== Iniciar servidor

def iniciar_servidor():
    uvicorn.run("controllers.nav_controller:app", port=8787, reload=True)
