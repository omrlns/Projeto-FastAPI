from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.sessao import sessao
from schemas import PedidoSchema
from models.models import Pedido

pedidos_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@pedidos_router.get("/")
async def pedidos():
    return {"mensagem": "se você está vendo isso, funcionou!"}

@pedidos_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": "pedido criado com sucesso! id do pedido: {}".format(novo_pedido.id)}

