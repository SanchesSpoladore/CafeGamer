from starlette.responses import Response

def adicionar_mensagem(response: Response, mensagem: str, tipo: str, titulo: str = ""):
    response.set_cookie(
        key="titulo",
        value=titulo,
        max_age=3,
        httponly=True,
        samesite="strict"
    )
    response.set_cookie(
        key="mensagem",
        value=mensagem,
        max_age=3,
        httponly=True,
        samesite="strict"
    )
    response.set_cookie(
        key="tipo",
        value=tipo,
        max_age=3,
        httponly=True,
        samesite="strict"
    )
