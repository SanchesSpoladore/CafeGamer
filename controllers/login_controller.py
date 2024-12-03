import hashlib
from controllers._db_controller import ControllerBase
from models.usuario_model import Usuario
    
def verificar_login(login : str, senha : str) -> Usuario:

    if validar_dados_login(login, senha):
        usuario = Usuario
        senha = hashlib.md5(f'{senha}'.encode()).hexdigest()
        query = f"""
        SELECT "IdUsuario", "Nome", "Nick", "Email", "Telefone", "CaminhoFoto", "DataNascimento", "IdUsuarioPermissao"
        FROM "Usuario" 
        WHERE ("Email" = '{login}' OR "Nick" = '{login}') AND "Senha" = '{senha}'"""
        retorno_usuario = ControllerBase.retorno_multiplo(query)
        
        if len(retorno_usuario) > 0:
            retorno_usuario = retorno_usuario[0]
            usuario.IdUsuario = retorno_usuario[0]
            usuario.Nome = retorno_usuario[1]
            usuario.Nick = retorno_usuario[2]
            usuario.Email = retorno_usuario[3]
            usuario.Telefone = retorno_usuario[4]
            usuario.CaminhoFoto = retorno_usuario[5]
            usuario.DataNascimento = retorno_usuario[6]
            usuario.IdUsuarioPermissao = retorno_usuario[7]

            return usuario
            
        else:
            return None

def validar_dados_login(login : str, senha : str) -> bool:

    palavras_reservadas = ["SELECT", "UPDATE", "DELETE", "INSERT", "DROP", "''", "--", "/*", "*/"]

    if not any(palavra_reservada in login.upper() for palavra_reservada in palavras_reservadas):
        if senha is not None and not senha.isspace():
            return True
    return False