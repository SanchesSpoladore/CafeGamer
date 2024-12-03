import shutil
from urllib import response
from fastapi import APIRouter, Body, File, Form, Path, Request, UploadFile, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from controllers.api_controller import atualizar_estado_usuario, excluir_usuario, obter_dados_usuario, obter_lista_usuarios
from controllers.cadastro_controller import salvar_cadastro
from controllers.forms_controller import salvar_reclamacao, salvar_sugestao, salvar_trabalhe_conosco
from controllers.perfil_controller import atualizar_dados_usuario
from routes.api_routes import get_lista_jogos, get_lista_pontuacao
from utils.auth import decodificar_token_autenticacao, remover_token_autenticacao
from utils.messages import adicionar_mensagem


router = APIRouter()
templates = Jinja2Templates(directory="templates")
router.mount("/static", StaticFiles(directory="static"), name="static")



#region USUARIO

@router.get("/usuario/perfil/{id_usuario}")
async def get_usuario_perfil(request: Request, id_usuario: int):
    mensagem = request.cookies.get("mensagem")
    tipo_mensagem = request.cookies.get("tipo")
    titulo = request.cookies.get("titulo")

    try:
        token = request.cookies.get("token_autenticacao")
        validacao = decodificar_token_autenticacao(token)
        if (validacao is not None and validacao.IdUsuario == id_usuario)or validacao.IdUsuarioPermissao == 3:
            usuario = obter_dados_usuario(id_usuario)
            return templates.TemplateResponse(
                "perfil.html", 
                {
                    "request": request, 
                    "mensagem": mensagem, 
                    "tipo_mensagem": tipo_mensagem,
                    "titulo": titulo,
                    "usuario": usuario
                }
            )
        else:
            return JSONResponse(status_code=403, content={"message": "Acesso não permitido"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})




@router.post("/usuario/atualizar_dados/{id_usuario}")
async def post_atualizar_usuario(
    id_usuario: int,
    nome: str = Form(...),
    email: str = Form(...),
    apelido: str = Form(...),
    telefone: str = Form(...),
    dataNascimento: str = Form(...),
    bio: str = Form(...),
    caminho_foto: UploadFile = File(None)
):
    # Tratamento do arquivo de imagem
    caminho_foto_final = None
    if caminho_foto:
        caminho_foto_final = f"static/uploads/{caminho_foto.filename}"
        with open(caminho_foto_final, "wb") as buffer:
            shutil.copyfileobj(caminho_foto.file, buffer)

    dados = {
        "nome": nome,
        "email": email,
        "apelido": apelido,
        "telefone": telefone,
        "dataNascimento": dataNascimento,
        "Descricao": bio,
        "caminho_foto": caminho_foto_final or "default/path/to/foto"
    }

    atualizar_dados_usuario(id_usuario, dados)
    return RedirectResponse(f"/usuario/perfil/{id_usuario}", status_code=303)
    
    
#endregion




#region RECLAME

@router.get("/usuario/reclame")
async def get_reclame(request: Request):
    mensagem = request.cookies.get("mensagem")
    tipo_mensagem = request.cookies.get("tipo")
    titulo = request.cookies.get("titulo")

    nome = request.cookies.get("nome", "")
    email = request.cookies.get("email", "")
    reclamacao = request.cookies.get("reclamacao", "")
    descricao = request.cookies.get("descricao", "")
    # imagem = request.cookies.get("imagem", "")

    return templates.TemplateResponse(
        "reclame.html", 
        {
            "request": request, 
            "mensagem": mensagem, 
            "tipo_mensagem": tipo_mensagem,
            "titulo": titulo,
            "nome": nome,
            "email": email,
            # "imagem": imagem
        }
    )


@router.post("/post_reclame")
async def post_reclame(
    response: RedirectResponse,
    name: str = Form(...), 
    email: str = Form(...),
    motivo: str = Form(...), 
    sugestao: str = Form(...)
    ):

    salvar_reclamacao(name, email, motivo, sugestao) 
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    return response

#endregion




#region TRABALHE
@router.get("/usuario/trabalheconosco")
async def get_trabalheconosco(request: Request):
    mensagem = request.cookies.get("mensagem")
    tipo_mensagem = request.cookies.get("tipo")
    titulo = request.cookies.get("titulo")

    nome = request.cookies.get("nome", "")
    email = request.cookies.get("email", "")
    
    return templates.TemplateResponse(
        "trabalheconosco.html", 
        {
            "request": request, 
            "mensagem": mensagem, 
            "tipo_mensagem": tipo_mensagem,
            "titulo": titulo,
            "nome": nome,
            "email": email
        }
    )

@router.post("/post_trabalheconosco")
async def post_trabalheconosco(
    response: RedirectResponse,
    name: str = Form(...), 
    email: str = Form(...),
    curriculo: str = Form(...)
    ):

    salvar_trabalhe_conosco(name, email, curriculo) 
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    return response

#endregion TRABALHE




#region SUGESTOES

@router.get("/usuario/sugestoes")
async def get_sugestoes(request: Request):
    mensagem = request.cookies.get("mensagem")
    tipo_mensagem = request.cookies.get("tipo")
    titulo = request.cookies.get("titulo")

    nome = request.cookies.get("nome", "")
    email = request.cookies.get("email", "")
    
    return templates.TemplateResponse(
        "sugestoes.html", 
        {
            "request": request, 
            "mensagem": mensagem, 
            "tipo_mensagem": tipo_mensagem,
            "titulo": titulo,
            "nome": nome,
            "email": email
        }
    )

@router.post("/post_sugestoes")
async def post_sugestoes(
    response: RedirectResponse,
    name: str = Form(...), 
    email: str = Form(...),
    sugestao: str = Form(...)
    ):

    salvar_sugestao(name, email, sugestao) 
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    return response


#endregion SUGESTOES




#region SAIR

@router.get("/sair")
async def get_sair(request: Request):
    response = RedirectResponse("/login", status.HTTP_303_SEE_OTHER)

    html = "<h6>Logout realizado</h6>"

    adicionar_mensagem(response, html, "warning", "Atenção")


    mensagem = request.cookies.get("mensagem")
    tipo_mensagem = request.cookies.get("tipo")
    titulo = request.cookies.get("titulo")

    # cookies_to_delete = [
    #     "nome", "nick", "email", "telefone", 
    #     "data_nascimento", "imagem", "senha"
    # ]

    # for cookie in cookies_to_delete:
    #     response.delete_cookie(key=cookie, path="/")


    response = templates.TemplateResponse(
        "login.html", 
        {
            "request": request, 
            "mensagem": mensagem, 
            "tipo_mensagem": tipo_mensagem,
            "titulo": titulo
        }
    )
    remover_token_autenticacao(response)

    return response




@router.get("/dados_usuario/{id_usuario}")
async def get_dados_usuario(request: Request, id_usuario: int):
    try:
        token = request.cookies.get("token_autenticacao")
        validacao = decodificar_token_autenticacao(token)
        if (validacao is not None and validacao.IdUsuario == id_usuario)or validacao.IdUsuarioPermissao == 3:
            usuario = obter_dados_usuario(id_usuario)
            return usuario
        else:
            return JSONResponse(status_code=403, content={"message": "Acesso não permitido"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


#endregion SAIR




#region ADMIN/BOSS

@router.get("/admin")
async def get_admin(request: Request):
    mensagem = request.cookies.get("mensagem")
    tipo_mensagem = request.cookies.get("tipo")
    titulo = request.cookies.get("titulo")

    lista_usuarios = obter_lista_usuarios()

    return templates.TemplateResponse(
        "admin.html", 
        {
            "request": request, 
            "mensagem": mensagem, 
            "tipo_mensagem": tipo_mensagem,
            "titulo": titulo,
            "lista_usuarios": lista_usuarios
        }
    )
    
@router.get("/boss")
async def get_boss(request: Request):
    lista_usuarios = obter_lista_usuarios()

    return templates.TemplateResponse(
        "boss.html", 
        {
            "request": request, 
            "lista_usuarios": lista_usuarios
        }
    )


@router.post("/admin/atualizar_estado_usuario/{id_usuario}")
async def post_atualizar_estado_usuario(id_usuario: int):
    await atualizar_estado_usuario(id_usuario)


@router.post("/boss/excluir_usuario/{id_usuario}")
async def post_excluir_usuario(id_usuario: int):
    await excluir_usuario(id_usuario)

#endregion


