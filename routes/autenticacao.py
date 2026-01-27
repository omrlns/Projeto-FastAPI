from fastapi import APIRouter, Depends
from models.models import Usuario
from dependencies.sessao import sessao

autenticacao_router = APIRouter(prefix="/autenticacao", tags=["autenticação"])

@autenticacao_router.get("/")
async def home():
    return {"mensagem": "se você está vendo isso, funcionou!", "autenticado": False}

@autenticacao_router.post("/criar_conta")
async def criar_conta(nome: str, email: str, senha: str, session = Depends(sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:
        return {"mensagem": "já existe um usuário com esse email."}
    else:
        novo_usuario = Usuario(nome, email, senha)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "usuário cadastrado com sucesso."}