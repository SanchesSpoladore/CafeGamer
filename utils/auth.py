from datetime import datetime, timedelta
import os
from typing import Optional
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
import jwt

from dto.usuario_autenticado import UsuarioAutenticado
from models.usuario_model import Usuario


def criar_token_autenticacao(usuario_autenticado: Usuario):
    dados_token = {
        "IdUsuario": usuario_autenticado.IdUsuario,
        "Nome": usuario_autenticado.Nome,
        "Email": usuario_autenticado.Email,
        "IdUsuarioPermissao": usuario_autenticado.IdUsuarioPermissao,
        "DataExpirarToken": (datetime.now() + timedelta(days=1)).timestamp()
    }
    SECRET_KEY = os.getenv("JWT_TOKEN_SECRET_KEY")
    return jwt.encode(dados_token, SECRET_KEY, algorithm="HS256")


def decodificar_token_autenticacao(token: str) -> Optional[UsuarioAutenticado]:
    SECRET_KEY = os.getenv("JWT_TOKEN_SECRET_KEY")
    try:
        dados_token = jwt.decode(token, SECRET_KEY, "HS256")
        return UsuarioAutenticado(
            IdUsuario = int(dados_token["IdUsuario"]),
            Nome = dados_token[ "Nome"],
            Email = dados_token["Email"],
            IdUsuarioPermissao = int(dados_token["IdUsuarioPermissao"])
        )
    # Erro de token expirado
    except:
        return None


def adicionar_token_autenticacao(response: RedirectResponse, token: str):
    response.set_cookie(
        key = "token_autenticacao",
        value = token,
        max_age = 86400, # Um dia
        httponly = True,
        samesite = "strict"
    )


def remover_token_autenticacao(response: RedirectResponse):
        
    cookies = [
        "token_autenticacao", "nome", "nick", "email", "data_nascimento", "imagem"
    ]

    for cookie in cookies:
        response.delete_cookie(key=cookie, path="/")
        # response.set_cookie(
        #     key = cookie,
        #     value = None,
        #     max_age = 0,
        #     httponly = True,
        #     samesite = "strict",
        # )


async def checar_autenticacao(request: Request, call_next):
    token = request.cookies.get("token_autenticacao", None)
    if token:
        usuario_autenticado = decodificar_token_autenticacao(token)
        if usuario_autenticado:  # Verifique se o token é válido
            request.state.usuario = usuario_autenticado
        else:
            request.state.usuario = None  # Token inválido ou expirado
    else:
        request.state.usuario = None  # Token ausente
    response = await call_next(request)
    return response


async def checar_autorizacao(request: Request):
    if (len(request.state._state) != 0):
        usuario = request.state.usuario 
    else:
        usuario = None
    rota = request.url.path

    # Define áreas com diferentes níveis de acesso
    area_usuario = rota.startswith("/usuario") or rota.startswith("/jogos")
    area_admin = rota.startswith("/admin")
    area_boss = rota.startswith("/api") or rota.startswith("/boss")

    # Usuario padrão = 1
    # Admin = 2
    # Master = 3

    if (area_usuario or area_admin or area_boss) and usuario is None:
        raise HTTPException(status_code=401, detail="Usuário não autenticado!")

    if area_admin and usuario.IdUsuarioPermissao == 1:
        raise HTTPException(status_code=403, detail="Usuário não autorizado!")

    if area_boss and usuario.IdUsuarioPermissao in [1,2]:
        raise HTTPException(status_code=403, detail="Usuário não autorizado!")