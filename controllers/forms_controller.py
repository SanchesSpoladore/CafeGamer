import hashlib
import os
import shutil

from controllers._db_controller import ControllerBase
from utils.helpers import hora_str

caminho_dados = "./arquivos/forms/"


def salvar_sugestao(nome: str, email: str, descricao: str):
    
    texto = f"""SUGESTÃO
    
    Nome: {nome}
    Email: {email}
    Descricao: {descricao}
    
    Data: {hora_str()}
    """
    
    salvar_formulario(f"reclame/SUGESTAO - {hora_str()}" ,texto)
    
    

def salvar_reclamacao(nome: str, email: str, motivo: str, descricao: str):
    
    texto = f"""RECLAMAÇÃO
    
    Nome: {nome}
    Email: {email}
    Motivo: {motivo}
    Descricao: {descricao}
    
    Data: {hora_str()}
    """
    
    salvar_formulario(f"reclame/RECLAMACAO - {hora_str()}" ,texto)


def salvar_trabalhe_conosco(nome: str, email: str, curriculum: str):
    
    hora = hora_str()
    
    # if curriculum and curriculum.filename and curriculum.size > 0:
    #     nome_arquivo = f"trabalhe/curriculum/CRC-{hora}.{curriculum.filename.split('.')[-1]}"
    
    #     caminho_curriculum = os.path.join(caminho_dados, nome_arquivo)
    #     with open(caminho_curriculum, "wb") as buffer:
    #         shutil.copyfileobj(curriculum.file, buffer)
    
    texto = f"""CURRICULUM
    
    Nome: {nome}
    Email: {email}
    Descricao curriculum: "{curriculum}"
    
    Data: {hora}
    """
    
    salvar_formulario(f"/trabalhe/CURRICULUM - {hora}" ,texto)


def salvar_formulario(nome_arquivo: str, texto: str):
    
    nome_arquivo = caminho_dados + "/" + nome_arquivo + ".txt"
    
    if not os.path.exists(caminho_dados):
        os.makedirs(caminho_dados)
    
    with open(nome_arquivo, "a") as arquivo:
        arquivo.write(texto)
    
