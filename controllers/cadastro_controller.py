import hashlib
import os
import shutil

from fastapi import File
from controllers._db_controller import ControllerBase

caminho_dados = "./store/pic/users"

def salvar_cadastro(nome: str, nick: str, email: str, telefone: str, data_nascimento: str, senha: str, imagem):
    
    senha = hashlib.md5(f'{senha}'.encode()).hexdigest()
    query = f"""INSERT INTO "Usuario" ("Email", "Senha", "IdUsuarioPermissao", "Nome", "Nick", "Telefone", "DataNascimento")
        VALUES ('{email}','{senha}',1,'{nome}','{nick}','{telefone}','{data_nascimento}')"""
    
    retorno_usuario = ControllerBase.retorno_ultimo_id(query)

    if imagem.filename != "" and imagem.size > 0 :
        nome_arquivo = f"user-{str(retorno_usuario)}.{str(imagem.content_type).replace("image/","")}"

        if not os.path.exists(caminho_dados):
            os.makedirs(caminho_dados)
    
        caminho_imagem = os.path.join(caminho_dados, nome_arquivo)
        with open(caminho_imagem, "wb") as buffer:
            shutil.copyfileobj(imagem.file, buffer)

        query = f"""UPDATE "Usuario" SET "CaminhoFoto" = '{nome_arquivo}' WHERE "IdUsuario" = {retorno_usuario} """
        ControllerBase.executar(query)


def verificar_cadastro_existente(nick: str, email: str):
    
    query = f"""
    SELECT "Nick", "Email"
    FROM "Usuario"
    WHERE ("Nick" = '{nick}' OR "Email" = '{email}')
    """
    return ControllerBase.retorno_unico(query)
    
