from fastapi import APIRouter

pedidos_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@pedidos_router.get("/")
async def pedidos():
    return {"mensagem": "se você está vendo isso, funcionou!"}