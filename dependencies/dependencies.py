from models.models import db
from sqlalchemy.orm import sessionmaker, Session
from models.models import Usuario
from fastapi import Depends

def sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session # retorna a sessão, mas não encerra a função
    finally: # independente do que acontecer, o finally vai ser executado
        session.close()

def verificar_token(token, session: Session = Depends(sessao)):
    # verificar se o token é válido e extrair o id do usuário do token
    usuario = session.query(Usuario).filter(Usuario.id==1).first()
    return usuario
