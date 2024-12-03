import hashlib
import os
import shutil

from fastapi import File
from controllers._db_controller import ControllerBase
from utils.helpers import hora_str

caminho_dados = "./store/src/messages"

def salvar_reclamacao(nome: str, email: str, reclamacao: str, descricao: str, imagem):
    
    msg = f"Nome: {nome}\nEmail: {email}\nHora: {hora_str()}\nReclamacao: {reclamacao}\nDescricao: {descricao}\n"

    with open(caminho_dados + "RECLAMACAO_" + hora_str() + ".txt", "a", encoding="utf-8") as arquivo_log:
        arquivo_log.write(msg)
    
