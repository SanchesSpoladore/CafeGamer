from dataclasses import dataclass
from typing import Optional

@dataclass

class Usuario:
    IdUsuario: Optional[int] = None
    Email: Optional[str] = None 
    IdUsuarioPermissao: Optional[int] = None 
    Nome: Optional[str] = None 
    Nick: Optional[str] = None 
    Telefone: Optional[str] = None 
    CaminhoFoto: Optional[str] = None 
    DataCadastro: Optional[str] = None 
    DataNascimento: Optional[str] = None 
    DataUltimoLogin: Optional[str] = None 
    Descricao: Optional[str] = None 
    Ativo: Optional[bool] = None
    
    
        