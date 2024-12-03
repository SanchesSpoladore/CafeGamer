import base64
from datetime import datetime
from io import BytesIO
from typing import List
from controllers._db_controller import ControllerBase
from dto.dados_record import DadosSalvarRecord
from models.lista_jogos_model import ListaJogos
from models.lista_pontuacao_model import ListaPontuacao
from models.usuario_model import Usuario
from captcha.image import ImageCaptcha


#region SELECT

def obter_lista_jogos() -> List[ListaJogos]:

    query = f"""
    SELECT "Nome", "CaminhoCapa", "QtdeCurtida", "QtdeAcessos", "MaiorPontuacao"
    FROM "Jogo" 
    WHERE "Excluido" = 0
    """
    resultados =  ControllerBase.retorno_multiplo(query)
    jogos = [
        ListaJogos (
            nome=resultado[0], 
            capajogo=resultado[1], 
            curtidas=resultado[2], 
            acessos=resultado[3], 
            record=resultado[4]
        ) 
        for resultado in resultados
    ]
    return jogos

def obter_lista_usuarios() -> List[Usuario] :

    query = f"""
    SELECT "IdUsuario", "Email", "Nome", "Nick", "Telefone", "CaminhoFoto", "DataCadastro", "DataNascimento", "DataUltimoAcesso", "Ativo"
    FROM "Usuario"
    WHERE "Excluido" = 0
    """
    resultados =  ControllerBase.retorno_multiplo(query)
    lista_usuarios = [
        Usuario (
            IdUsuario = resultado[0], 
            Email = resultado[1], 
            Nome = resultado[2], 
            Nick = resultado[3], 
            Telefone = resultado[4], 
            CaminhoFoto = resultado[5], 
            DataCadastro = resultado[6], 
            DataNascimento = resultado[7], 
            DataUltimoLogin = resultado[8],
            Ativo = resultado[9]
        ) 
        for resultado in resultados
    ]
    return lista_usuarios

def obter_records_jogador(id_usuario: int):

    query = f"""
    SELECT j."Nome", j."CaminhoCapa", jp."Pontuacao", jp."DataPontuacao"
    FROM "JogoPontuacao" jp
        LEFT JOIN "Jogo" j ON j."IdJogo" = jp."IdJogo"
        LEFT JOIN "Usuario" u ON u."IdUsuario" = jp."IdUsuario"
    WHERE jp."PontuacaoValida" = 1
    AND j."Excluido" = 0
    AND u."Excluido" = 0
    AND u."IdUsuario" = {id_usuario}
    """
    resultado = ControllerBase.retorno_multiplo(query)
    return resultado

def obter_records_rodape() -> List[ListaPontuacao]:

    query = """
    SELECT u."Nome", u."Nick", j."Nome", j."CaminhoCapa", jp."Pontuacao", jp."DataPontuacao"
    FROM "JogoPontuacao" jp
        LEFT JOIN "Jogo" j ON j."IdJogo" = jp."IdJogo"
        LEFT JOIN "Usuario" u ON u."IdUsuario" = jp."IdUsuario"
    WHERE jp."PontuacaoValida" = 1
    AND j."Excluido" = 0
    AND u."Excluido" = 0
    ORDER BY jp."DataPontuacao" DESC
    LIMIT 10
    """

    resultados = ControllerBase.retorno_multiplo(query)
    lista_pontuacao = [
        ListaPontuacao (
            nome = resultado[0],
            nick = resultado[1],
            jogo = resultado[2],
            capajogo = resultado[3],
            pontuacao = resultado[4],
            datapontuacao = datetime.strptime(resultado[5], '%Y-%m-%d %H:%M:%S').date()
        )
        for resultado in resultados
    ]
    return lista_pontuacao

def obter_dados_usuario(id_usuario: int) -> Usuario:

    query = f"""
    SELECT "IdUsuario", "Email", "IdUsuarioPermissao ",
    "Nome", "Nick", "Telefone", "CaminhoFoto",
    "DataCadastro", "DataNascimento", "DataUltimoLogin", "Descricao"
    FROM "Usuario"
    WHERE "IdUsuario" = {id_usuario} 
    """

    resultado = ControllerBase.retorno_multiplo(query)[0]
    dados_usuario = Usuario (
        IdUsuario = resultado[0],
        Email = resultado[1],
        IdUsuarioPermissao = resultado[2],
        Nome = resultado[3],
        Nick = resultado[4],
        Telefone = resultado[5],
        CaminhoFoto = resultado[6],
        DataCadastro = resultado[7],
        DataNascimento = resultado[8],
        DataUltimoLogin = resultado[9],
        Descricao = resultado[10]
    ) 

    return dados_usuario

#endregion SELECT




#region UPDATE

async def atualizar_curtidas(nome_jogo: str):

    query = f"""
    UPDATE "Jogo" SET "QtdeCurtida" = "QtdeCurtida" + 1
    WHERE "Nome" = '{nome_jogo}'
    """
    ControllerBase.executar(query)

async def atualizar_acessos(nome_jogo: str):

    query = f"""
    UPDATE "Jogo" SET "QtdeAcessos" = "QtdeAcessos" + 1
    WHERE "Nome" = '{nome_jogo}'
    """
    ControllerBase.executar(query)

async def registrar_record(dados: DadosSalvarRecord):

    query = f"""
    INSERT INTO "JogoPontuacao" ("IdJogo", "IdUsuario", "Pontuacao", "DataPontuacao", "PontuacaoValida", "IdUsuarioModeracao") VALUES
    (
        (SELECT "IdJogo" FROM "Jogo" WHERE "Nome" = '{dados.nome_jogo}'),
        {dados.id_usuario},
        {dados.pontuacao},
        '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',
        1,
        3
    )
    """
    ControllerBase.executar(query)

async def atualizar_estado_usuario(id_usuario: int):

    query = f"""
    UPDATE "Usuario" SET "Ativo" = ("Ativo" * -1) + 1
    WHERE "IdUsuario" = {id_usuario}
    """
    ControllerBase.executar(query)

async def excluir_usuario(id_usuario: int):

    query = f"""
    UPDATE "Usuario" SET "Excluido" = 1
    WHERE "IdUsuario" = {id_usuario}
    """
    ControllerBase.executar(query)

#endregion UPDATE




#region FUNCOES AUXILIARES

def gerar_captcha():
    captcha_image = ImageCaptcha(width=280, height=90)
    captcha_bytes = BytesIO()
    captcha_image.write("IFES", captcha_bytes) 

    captcha_base64 = base64.b64encode(captcha_bytes.getvalue()).decode("utf-8")
    captcha_src = f"data:image/png;base64,{captcha_base64}"
    return captcha_src

#endregion