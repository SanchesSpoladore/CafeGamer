from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from controllers.api_controller import *
from random import shuffle

router = APIRouter(prefix="/api")

# ============== End Points

@router.get("/lista_jogos")
async def get_lista_jogos():
    try:
        lista = obter_lista_jogos()
        shuffle(lista)
        return lista
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@router.get("/lista_pontuacao")
async def get_lista_pontuacao():
    try:
        lista = obter_records_rodape()
        shuffle(lista)
        return lista
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

# @router.get("/records")
# async def get_records():
#     try:
#         pontuacoes = obter_records_rodape()
#         return JSONResponse(content=pontuacoes)
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"message": str(e)})
    
    
@router.get("/pesquisa")
async def get_pesquisa(s: str):
    try:
        resultados = ["Space Invaders", "Pac-Man", "Corrida de Cavalos", "Cobrinha"]
        sugestoes = [jogo for jogo in resultados if s.lower() in jogo.lower()]
        return JSONResponse(content=sugestoes)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})