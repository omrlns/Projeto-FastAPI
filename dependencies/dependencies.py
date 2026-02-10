from models.models import db
from sqlalchemy.orm import sessionmaker, Session
from models.models import Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema

def sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session # retorna a sessão, mas não encerra a função
    finally: # independente do que acontecer, o finally vai ser executado
        session.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(sessao)):
    # verificar se o token é válido e extrair o id do usuário do token
    try:
        informacoes = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(informacoes.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token.")
    
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido.")
    return usuario