from fastapi import APIRouter, Depends, HTTPException
from models.models import Usuario
from dependencies.sessao import sessao
from main import bcrypt_context

autenticacao_router = APIRouter(prefix="/autenticacao", tags=["autenticação"])

@autenticacao_router.get("/")
async def home():
    return {"mensagem": "se você está vendo isso, funcionou!", "autenticado": False}

@autenticacao_router.post("/criar_conta")
async def criar_conta(nome: str, email: str, senha: str, session = Depends(sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="e-mail do usuário já cadastrado!")
    else:
        senha_criptografada = bcrypt_context.hash(senha)
        novo_usuario = Usuario(nome, email, senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "usuário cadastrado com sucesso: {}".format(email)}