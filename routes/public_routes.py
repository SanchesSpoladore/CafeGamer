import base64
from io import BytesIO
from fastapi import APIRouter, File, Form, Request, UploadFile, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException



from controllers.cadastro_controller import salvar_cadastro, verificar_cadastro_existente
from controllers.forms_controller import salvar_reclamacao
from controllers.login_controller import verificar_login
from dto.usuario_autenticado import UsuarioAutenticado
from models.usuario_model import Usuario
from routes.api_routes import *
from utils.auth import adicionar_token_autenticacao, criar_token_autenticacao, decodificar_token_autenticacao
from utils.messages import adicionar_mensagem


router = APIRouter()
templates = Jinja2Templates(directory="templates")
router.mount("/static", StaticFiles(directory="static"), name="static")
router.mount("/static/img/capas", StaticFiles(directory="static/img/capas"), name="capas")

usuario_autenticado = Usuario



#region ROOT

@router.get("/")
async def index(request: Request):
    mensagem = request.cookies.get("mensagem")
    tipo_mensagem = request.cookies.get("tipo")
    titulo = request.cookies.get("titulo")

    jogos = await get_lista_jogos()
    pontuacao = await get_lista_pontuacao()
    return templates.TemplateResponse(
        "home.html", 
        {
            "request": request, 
            "mensagem": mensagem, 
            "tipo_mensagem": tipo_mensagem,
            "titulo": titulo,
            "titulo": "Home", 
            "pagina": "Home", 
            "lista_jogos": jogos , 
            "lista_pontuacao": pontuacao,
            "javaccript": "home"
        }
    )
    
#endregion




#region LOGIN 
@router.get("/login")
async def login(request: Request):

    token = request.cookies.get("token_autenticacao")

    if (token is not None):
        response = RedirectResponse("/", status.HTTP_307_TEMPORARY_REDIRECT)
        html = "<h6>Verifique as informações:</h6><ul>"
        html += f"<li>Realize o loggout para realizar um novo login.</li>"

        adicionar_mensagem(response, html, "danger", "Usuário já logado")

        return response

    mensagem = request.cookies.get("mensagem")
    tipo_mensagem = request.cookies.get("tipo")
    titulo = request.cookies.get("titulo")

    login = request.cookies.get("email", "")
    senha = request.cookies.get("senha", "")

    return templates.TemplateResponse(
        "login.html", 
        {
            "request": request, 
            "mensagem": mensagem, 
            "tipo_mensagem": tipo_mensagem,
            "titulo": titulo,
            "login": login,
            "senha": senha
        }
    )
    
@router.post("/post_login")
async def post_login(
    response: RedirectResponse,
    login: str = Form(...), 
    senha: str = Form(...)
    ):

    usuario_autenticado = verificar_login(login,senha)
    if login == "gabriel@email.com":
        response = RedirectResponse("/login", status.HTTP_303_SEE_OTHER)

        html = "<h6>Avisar o usuario 'Gabriel' pra mudar a senha'123'!</h6>"

        response.set_cookie("login", login, max_age=3)
        response.set_cookie("senha", senha, max_age=3)

        adicionar_mensagem(response, html, "danger", "Erro")

        return response
    
    
    elif usuario_autenticado:

        token = criar_token_autenticacao(usuario_autenticado)

        response =  RedirectResponse("/", status.HTTP_303_SEE_OTHER)
        
        adicionar_token_autenticacao(response,token)
        response.delete_cookie("login")
        response.delete_cookie("senha")

        html = f"<h6>Login realizado!</h6><br><p>Salve salve {usuario_autenticado.Nome}</p>"
        
        response.set_cookie("id_usuario", usuario_autenticado.IdUsuario)
        response.set_cookie("id_usuario_permissao", usuario_autenticado.IdUsuarioPermissao)
        response.set_cookie("nome", usuario_autenticado.Nome)
        response.set_cookie("nick", usuario_autenticado.Nick)
        response.set_cookie("email", usuario_autenticado.Email)
        response.set_cookie("data_nascimento", usuario_autenticado.DataNascimento)
        response.set_cookie("imagem", usuario_autenticado.CaminhoFoto)

        adicionar_mensagem(response, html, "success", "Sucesso!")

        return response

    else:
        response = RedirectResponse("/login", status.HTTP_303_SEE_OTHER)

        html = "<h6>Dados inválidos!</h6>"

        response.set_cookie("login", login, max_age=3)
        response.set_cookie("senha", senha, max_age=3)

        adicionar_mensagem(response, html, "danger", "Erro")

        return response
    
#endregion LOGIN




#region CADASTRO
@router.get("/cadastro")
async def cadastro(request: Request):

    token = request.cookies.get("token_autenticacao")

    if (token is not None):
        response = RedirectResponse("/", status.HTTP_307_TEMPORARY_REDIRECT)
        html = "<h6>Verifique as informações:</h6><ul>"
        html += f"<li>Realize o loggout para realizar um novo cadastro.</li>"

        adicionar_mensagem(response, html, "danger", "Usuário já logado")

        return response
    
    captcha = gerar_captcha()

    mensagem = request.cookies.get("mensagem")
    tipo_mensagem = request.cookies.get("tipo")
    titulo = request.cookies.get("titulo")

    nome = request.cookies.get("nome", "")
    nick = request.cookies.get("nick", "")
    email = request.cookies.get("email", "")
    telefone = request.cookies.get("telefone", "")
    data_nascimento = request.cookies.get("data_nascimento", "")
    imagem = request.cookies.get("imagem", "")

    return templates.TemplateResponse(
        "cadastro.html", 
        {
            "request": request, 
            "mensagem": mensagem, 
            "tipo_mensagem": tipo_mensagem,
            "titulo": titulo,
            "nome": nome,
            "nick": nick,
            "email": email,
            "telefone": telefone,
            "data_nascimento": data_nascimento,
            "imagem": imagem,
            "captcha": captcha
        }
    )


@router.post("/post_cadastro")
async def post_cadastro(
    response: RedirectResponse,
    nome: str = Form(...), 
    nick: str = Form(...), 
    email: str = Form(...),
    telefone: str = Form(None), 
    data_nascimento: str = Form(...), 
    senha: str = Form(...), 
    confirmacao_senha: str = Form(...),
    resposta_captcha: str = Form(...),
    imagem: UploadFile = File(None)
    ):

    erros = []

    if resposta_captcha.upper() != "IFES": 
        response = RedirectResponse("/cadastro", status.HTTP_303_SEE_OTHER)

        erros.append("Captcha inválido!.")
        html = "<h6>Verifique as informações:</h6><ul>"
        for erro in erros:
            html += f"<li>{erro}</li>"
        html += "</ul>"

        response.set_cookie("nome", nome, max_age=3)
        response.set_cookie("nick", nick, max_age=3)
        response.set_cookie("email", email, max_age=3)
        response.set_cookie("telefone", (telefone if telefone is not None else ""), max_age=3)
        response.set_cookie("data_nascimento", data_nascimento, max_age=3)
        response.set_cookie("imagem", imagem, max_age=3)

        adicionar_mensagem(response, html, "danger", "Erro")

        return response

    if verificar_cadastro_existente(nick, email):
        response = RedirectResponse("/cadastro", status.HTTP_303_SEE_OTHER)

        if nick == "usuario" or email == "teste@email.com":
            erros.append(f"Usuário 'Pizetta' já utiliza a senha '123'. Tente outra senha!")
            html = "<h6>Verifique as informações:</h6><ul>"
            for erro in erros:
                html += f"<li>{erro}</li>"
            html += "</ul>"

            adicionar_mensagem(response, html, "danger", "Meme kkkkk")

            return response

        erros.append(f"Usuário já existente.")
        html = "<h6>Verifique as informações:</h6><ul>"
        for erro in erros:
            html += f"<li>{erro}</li>"
        html += "</ul>"

        response.set_cookie("nome", nome, max_age=3)
        response.set_cookie("nick", nick, max_age=3)
        response.set_cookie("email", email, max_age=3)
        response.set_cookie("telefone", (telefone if telefone is not None else ""), max_age=3)
        response.set_cookie("data_nascimento", data_nascimento, max_age=3)
        response.set_cookie("imagem", imagem, max_age=3)

        adicionar_mensagem(response, html, "danger", "Erro")

        return response

    if senha == confirmacao_senha:
        salvar_cadastro(nome, nick, email, telefone, data_nascimento, senha, imagem)

        response =  RedirectResponse("/login", status.HTTP_303_SEE_OTHER)
        response.set_cookie("email", email, max_age=3)
        html = "<h6>Cadastro realizado!</h6>"
        adicionar_mensagem(response, html, "success", "Sucesso!")

        return response

    else:
        response = RedirectResponse("/cadastro", status.HTTP_303_SEE_OTHER)

        erros.append("As senhas não correspondem.")
        html = "<h6>Verifique as informações:</h6><ul>"
        for erro in erros:
            html += f"<li>{erro}</li>"
        html += "</ul>"

        response.set_cookie("nome", nome, max_age=3)
        response.set_cookie("nick", nick, max_age=3)
        response.set_cookie("email", email, max_age=3)
        response.set_cookie("telefone", (telefone if telefone is not None else ""), max_age=3)
        response.set_cookie("data_nascimento", data_nascimento, max_age=3)
        response.set_cookie("imagem", imagem, max_age=3)

        adicionar_mensagem(response, html, "danger", "Erro")

        return response

#endregion CADASTRO





#region SOBRE
@router.get("/sobre")
async def index(request: Request):
    jogos = await get_lista_jogos()
    pontuacao = await get_lista_pontuacao()
    return templates.TemplateResponse(
        "sobre.html", 
        {
            "request": request, 
            "titulo": "Sobre", 
            "pagina": "sobre", 
            "lista_jogos": jogos , 
            "lista_pontuacao": pontuacao
        }
    )

#endregion SOBRE



#region EMBREVE
@router.get("/embreve")
async def index(request: Request):
    return templates.TemplateResponse(
        "embreve.html", 
        {
            "request": request, 
            "titulo": "Em breve", 
            "pagina": "embreve"
        }
    )

#endregion SOBRE

    