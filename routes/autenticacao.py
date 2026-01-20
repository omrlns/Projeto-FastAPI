from fastapi import APIRouter

autenticacao_router = APIRouter(prefix="/autenticacao", tags=["autenticação"])

@autenticacao_router.get("/")
async def autenticar():
    return {"mensagem": "se você está vendo isso, funcionou!", "autenticado": False}