from fastapi import APIRouter, Depends, HTTPException
from models.models import Usuario
from dependencies.sessao import sessao
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session

def criar_token(id_usuario):
    token = "aeioubcdfgh{}".format(id_usuario)
    return token 


autenticacao_router = APIRouter(prefix="/autenticacao", tags=["autenticação"])

@autenticacao_router.get("/")
async def home():
    return {"mensagem": "se você está vendo isso, funcionou!", "autenticado": False}

@autenticacao_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="e-mail do usuário já cadastrado!")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        
        novo_usuario = Usuario(usuario_schema.nome, 
                               usuario_schema.email, 
                               senha_criptografada, 
                               usuario_schema.perfilAtivo, 
                               usuario_schema.perfilAdmin)
        
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "usuário cadastrado com sucesso: {}".format(usuario_schema.email)}

@autenticacao_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="usuário não encontrado.")
    else:
        acessar_token = criar_token(usuario.id)
        return {"acessar_token": acessar_token,
                "tipo_token": "Bearer"}
