from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies.dependencies import sessao, verificar_token
from schemas import PedidoSchema
from models.models import Pedido, Usuario

pedidos_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

@pedidos_router.get("/")
async def pedidos():
    return {"mensagem": "se você está vendo isso, funcionou!"}

@pedidos_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": "pedido criado com sucesso! id do pedido: {}".format(novo_pedido.id)}

@pedidos_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(sessao), usuario: Usuario = Depends(verificar_token)):
    # se usuario.perfilAdmin = True e se usuario.id == pedido.usuario, são duas verificações que eu irei fazer para validar a requisição
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido: 
        raise HTTPException(status_code=400, detail="Pedido não encontrado!")
    if not usuario.perfilAdmin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação!")
    pedido.status = "CANCELADO"
    session.commit()
    return {"mensagem": "Pedido #{} cancelado com sucesso!".format(id_pedido),
            "pedido": pedido
            }

