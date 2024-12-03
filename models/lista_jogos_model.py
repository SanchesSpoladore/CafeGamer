from dataclasses import dataclass

@dataclass 

class ListaJogos():
    nome: str
    capajogo: str
    curtidas: int
    acessos: int
    record: float