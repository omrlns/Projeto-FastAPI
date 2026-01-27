from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    perfilAtivo: Optional[bool]
    perfilAdmin: Optional[bool]

    class Config:
        from_attributes = True

class PedidoSchema(BaseModel):
    id_usuario = int

    class Config:
        from_attributes = True