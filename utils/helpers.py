import datetime

NOME_PASTA_HTML = "./nav/"
NOME_PASTA_LOG = "./store/log/"

def hora():
    return datetime.datetime.now()

def hora_str():
    return str(datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S"))

def log_banco(msg: str):
    pass
    # with open(NOME_PASTA_LOG + "database/" + "BANCO_" + hora_str() + ".txt", "a", encoding="utf-8") as arquivo_log:
    #     arquivo_log.write(f"[{hora_str()}] - {msg}\n")


def excecao(msg : str, erro : Exception = None, msgextra : str = None):
    if(erro is None):
        with open(NOME_PASTA_LOG + "GENERIC_" + hora_str() + ".txt", "a", encoding="utf-8") as arquivo_log:
            arquivo_log.write(f"[{hora_str()}] - {msg}\n")
        return
    else:
        if(msgextra is None):
            with open(NOME_PASTA_LOG + hora()) as arquivo_log:
                arquivo_log.write(f"[{hora_str()}] - {msg}\n\n{erro}")
        else:
            with open(NOME_PASTA_LOG + hora()) as arquivo_log:
                arquivo_log.write(f"[{hora_str()}] - {msg}\n\n{msgextra}\n\n{erro}")

def ler_html(nome_arquivo: str) -> str:
    caminho_arquivo_html = f"{NOME_PASTA_HTML}{nome_arquivo}.html"
    with open(caminho_arquivo_html, "r", encoding="utf-8") as arquivo:
        conteudo_html = arquivo.read()
    return conteudo_html


def ler_html_index(nome_arquivo: str) -> str:
    caminho_arquivo_html = f"{NOME_PASTA_HTML}{nome_arquivo}/index.html"
    with open(caminho_arquivo_html, "r", encoding="utf-8") as arquivo:
        return arquivo.read()

