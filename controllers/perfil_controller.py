import hashlib
import os
import shutil

from controllers._db_controller import ControllerBase
from utils.helpers import hora_str



def atualizar_dados_usuario(id_usuario: int, dados: dict):
    query = f"""
    UPDATE "Usuario"
    SET "Nome" = '{dados['nome']}',
        "Email" = '{dados['email']}',
        "Telefone" = '{dados['telefone']}',
        "Apelido" = '{dados['apelido']}',
        "Descricao" = '{dados['bio']}'
    WHERE "IdUsuario" = {id_usuario}
    """
    ControllerBase.executar(query)



    
    
