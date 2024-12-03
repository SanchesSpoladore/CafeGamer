from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from controllers.api_controller import atualizar_acessos, atualizar_curtidas, registrar_record
from dto.dados_record import DadosSalvarRecord
from routes.api_routes import get_lista_jogos, get_lista_pontuacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")
router.mount("/static", StaticFiles(directory="static"), name="static")
router.mount("/template/jogos", StaticFiles(directory="templates/jogos"), name="jogos")


# ============== Rotas jogos

@router.get("/jogos/Snake")
async def get_snake(request: Request):
    nome_jogo = "Snake"
    jogos = await get_lista_jogos()
    pontuacao = await get_lista_pontuacao()
    await atualizar_acessos(nome_jogo)
    return templates.TemplateResponse("/jogo.html", {"request": request, "titulo": "Snake", "pagina": "Home", "caminho_jogo": "Snake/index.html", "nome_jogo": nome_jogo, "lista_jogos": jogos , "lista_pontuacao": pontuacao})


@router.get("/jogos/Dino")
async def get_dino(request: Request):
    nome_jogo = "Dino"
    jogos = await get_lista_jogos()
    pontuacao = await get_lista_pontuacao()
    await atualizar_acessos(nome_jogo)
    return templates.TemplateResponse("/jogo.html", {"request": request, "titulo": "Dino", "pagina": "Home", "caminho_jogo": "Dino/index.html", "nome_jogo": nome_jogo, "lista_jogos": jogos , "lista_pontuacao": pontuacao})


@router.get("/jogos/BatalhaNaval")
async def get_batalha_naval(request: Request):
    nome_jogo = "BatalhaNaval"
    jogos = await get_lista_jogos()
    pontuacao = await get_lista_pontuacao()
    await atualizar_acessos(nome_jogo)
    return templates.TemplateResponse("/jogo.html", {"request": request, "titulo": "BatalhaNaval", "pagina": "Home", "caminho_jogo": "BatalhaNaval/index.html", "nome_jogo": nome_jogo, "lista_jogos": jogos , "lista_pontuacao": pontuacao})


@router.get("/jogos/SpaceInvaders")
async def get_space_invaders(request: Request):
    nome_jogo = "SpaceInvaders"
    jogos = await get_lista_jogos()
    pontuacao = await get_lista_pontuacao()
    await atualizar_acessos(nome_jogo)
    return templates.TemplateResponse("/jogo.html", {"request": request, "titulo": "SpaceInvaders", "pagina": "Home", "caminho_jogo": "SpaceInvaders/index.html", "nome_jogo": nome_jogo, "lista_jogos": jogos , "lista_pontuacao": pontuacao})
    # jogos = await get_lista_jogos()
    # pontuacao = await get_lista_pontuacao()
    # await atualizar_acessos("SpaceInvaders")
    # return templates.TemplateResponse("/jogo.html", {"request": request, "titulo": "Space Invaders", "pagina": "Home", "caminho_jogo": "SpaceInvaders/index.html", "lista_jogos": jogos , "lista_pontuacao": pontuacao})


@router.get("/jogos/PacMan")
async def get_pac_man(request: Request):
    nome_jogo = "PacMan"
    jogos = await get_lista_jogos()
    pontuacao = await get_lista_pontuacao()
    await atualizar_acessos(nome_jogo)
    return templates.TemplateResponse("/jogo.html", {"request": request, "titulo": "PacMan", "pagina": "Home", "caminho_jogo": "PacMan/index.html", "nome_jogo": nome_jogo, "lista_jogos": jogos , "lista_pontuacao": pontuacao})


@router.get("/jogos/CampoMinado")
async def get_campo_minado(request: Request):
    nome_jogo = "CampoMinado"
    jogos = await get_lista_jogos()
    pontuacao = await get_lista_pontuacao()
    await atualizar_acessos(nome_jogo)
    return templates.TemplateResponse("/jogo.html", {"request": request, "titulo": "CampoMinado", "pagina": "Home", "caminho_jogo": "CampoMinado/index.html", "nome_jogo": nome_jogo, "lista_jogos": jogos , "lista_pontuacao": pontuacao})


@router.get("/jogos/CorridaCavalo")
async def get_corrida_cavalo(request: Request):
    nome_jogo = "CorridaCavalo"
    jogos = await get_lista_jogos()
    pontuacao = await get_lista_pontuacao()
    await atualizar_acessos(nome_jogo)
    return templates.TemplateResponse("/jogo.html", {"request": request, "titulo": "CorridaCavalo", "pagina": "Home", "caminho_jogo": "CorridaCavalo/index.html", "nome_jogo": nome_jogo, "lista_jogos": jogos , "lista_pontuacao": pontuacao})


@router.get("/jogos/DuckHunt")
async def get_duck_hunt(request: Request):
    nome_jogo = "DuckHunt"
    jogos = await get_lista_jogos()
    pontuacao = await get_lista_pontuacao()
    await atualizar_acessos(nome_jogo)
    return templates.TemplateResponse("/jogo.html", {"request": request, "titulo": "DuckHunt", "pagina": "Home", "caminho_jogo": "DunkHunt/index.html", "nome_jogo": nome_jogo, "lista_jogos": jogos , "lista_pontuacao": pontuacao})


@router.get("/jogos/ColorBlast")
async def get_color_blast(request: Request):
    nome_jogo = "ColorBlast"
    jogos = await get_lista_jogos()
    pontuacao = await get_lista_pontuacao()
    await atualizar_acessos(nome_jogo)
    return templates.TemplateResponse("/jogo.html", {"request": request, "titulo": "ColorBlast", "pagina": "Home", "caminho_jogo": "ColorBlast/index.html", "nome_jogo": nome_jogo, "lista_jogos": jogos , "lista_pontuacao": pontuacao})


@router.get("/jogos/Dama")
async def get_dama(request: Request):
    nome_jogo = "Dama"
    jogos = await get_lista_jogos()
    pontuacao = await get_lista_pontuacao()
    await atualizar_acessos(nome_jogo)
    return templates.TemplateResponse("/jogo.html", {"request": request, "titulo": "Dama", "pagina": "Home", "caminho_jogo": "Dama/index.html", "nome_jogo": nome_jogo, "lista_jogos": jogos , "lista_pontuacao": pontuacao})


@router.get("/jogos/JogoDaVelha")
async def get_jogo_da_velha(request: Request):
    nome_jogo = "JogoDaVelha"
    jogos = await get_lista_jogos()
    pontuacao = await get_lista_pontuacao()
    await atualizar_acessos(nome_jogo)
    return templates.TemplateResponse("/jogo.html", {"request": request, "titulo": "JogoDaVelha", "pagina": "Home", "caminho_jogo": "JogoDaVelha/index.html", "nome_jogo": nome_jogo, "lista_jogos": jogos , "lista_pontuacao": pontuacao})


@router.get("/jogos/Xadrez")
async def get_xadrez(request: Request):
    nome_jogo = "Xadrez"
    jogos = await get_lista_jogos()
    pontuacao = await get_lista_pontuacao()
    await atualizar_acessos(nome_jogo)
    return templates.TemplateResponse("/jogo.html", {"request": request, "titulo": "Xadrez", "pagina": "Home", "caminho_jogo": "Xadrez/index.html", "nome_jogo": nome_jogo, "lista_jogos": jogos , "lista_pontuacao": pontuacao})


@router.get("/jogos/PedraPapelTesoura")
async def get_pedra_papel_tesoura(request: Request):
    nome_jogo = "PedraPapelTesoura"
    jogos = await get_lista_jogos()
    pontuacao = await get_lista_pontuacao()
    await atualizar_acessos(nome_jogo)
    return templates.TemplateResponse("/jogo.html", {"request": request, "titulo": "PedraPapelTesoura", "pagina": "Home", "caminho_jogo": "PedraPapelTesoura/index.html", "nome_jogo": nome_jogo, "lista_jogos": jogos , "lista_pontuacao": pontuacao})


# ============== Rotas auxiliares

@router.post("/jogos/curtir_jogo/{nome_jogo}")
async def post_curtir_jogo(nome_jogo: str):
    await atualizar_curtidas(nome_jogo)
    
@router.post("/jogos/SalvarRecord")
async def post_salvar_record(dados: DadosSalvarRecord):
    await registrar_record(dados)