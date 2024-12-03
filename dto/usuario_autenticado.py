from dataclasses import dataclass
from typing import Optional

@dataclass

class UsuarioAutenticado:
    IdUsuario: Optional[int] = None
    Nome: Optional[str] = None
    Email: Optional[str] = None
    IdUsuarioPermissao: Optional[int] = None