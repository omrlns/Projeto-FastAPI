from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies.dependencies import sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from models.models import Pedido, Usuario, ItemPedido

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
    return {
        "mensagem": "Pedido #{} cancelado com sucesso!".format(pedido.id),
        "pedido": pedido
            }

@pedidos_router.get("/listar")
async def listar_pedidos(session: Session = Depends(sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.perfilAdmin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação!")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }

@pedidos_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int,
                                item_pedido_schema: ItemPedidoSchema, 
                                session: Session = Depends(sessao), 
                                usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existente!")
    if not usuario.perfilAdmin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação!")
    item_pedido = ItemPedido(item_pedido_schema.quantidade,
                             item_pedido_schema.sabor,
                             item_pedido_schema.tamanho,
                             item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "Item criado com sucesso!",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }

@pedidos_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int,
                                session: Session = Depends(sessao), 
                                usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Esse item não existe no pedido!")
    if not usuario.perfilAdmin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação!")
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "Item removido com sucesso!",
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
        }

# finalizar pedido
# visualizar pedido
# visualizar todos os pedidos de um determinado usuário
