from _db._db_connection import conectar, verificar_banco
from utils.helpers import log_banco

class ControllerBase:

    @staticmethod
    def executar(query,paran=None):
        conexao = conectar()
        conexao.autocommit = True
        cursor = conexao.cursor()
        if paran:
            log_banco(f"Executada query:\n{query}\n\nParametros:{paran}")
            cursor.execute(query,(paran))
        else:
            log_banco(f"Executada query:\n{query}")
            cursor.execute(query)
        cursor.close()

    @staticmethod
    def retorno_unico(query):
        conexao = conectar()
        conexao.autocommit = True
        cursor = conexao.cursor()
        log_banco(f"Executada query:\n{query}")
        cursor.execute(query)
        resultado = cursor.fetchone()
        cursor.close()
        return resultado

    @staticmethod
    def retorno_multiplo(query):
        conexao = conectar()
        conexao.autocommit = True
        cursor = conexao.cursor()
        log_banco(f"Executada query:\n{query}")
        cursor.execute(query)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado

    @staticmethod
    def retorno_ultimo_id(query):
        conexao = conectar()
        conexao.autocommit = True
        cursor = conexao.cursor()
        log_banco(f"Executada query:\n{query}")
        cursor.execute(query)
        ultimo_id = cursor.lastrowid
        cursor.close()
        return ultimo_id


class Inicio():
    verificar_banco()


    
