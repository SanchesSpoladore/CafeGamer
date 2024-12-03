from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass 

class ListaPontuacao():
    nome: str
    nick: str
    jogo: str
    capajogo: str
    pontuacao: float
    datapontuacao: Optional[date]