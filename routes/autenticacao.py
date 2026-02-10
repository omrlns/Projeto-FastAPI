from fastapi import APIRouter, Depends, HTTPException
from models.models import Usuario
from dependencies.sessao import sessao
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


def criar_token(id_usuario):
    data_expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # sub, nome padrão para se referenciar ao dono do token
    # exp, para se referir a validade do token
    informacoes = {"sub": id_usuario, "exp": int(data_expiracao.timestamp())}
    jwt_codificado = jwt.encode(informacoes, SECRET_KEY, ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

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
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="usuário não encontrado ou credencias inválidas!")
    else:
        acessar_token = criar_token(usuario.id)
        return {"acessar_token": acessar_token,
                "tipo_token": "Bearer"}
