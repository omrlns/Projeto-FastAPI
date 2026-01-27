from models.models import db
from sqlalchemy.orm import sessionmaker

def sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session # retorna a sessão, mas não encerra a função
    finally: # independente do que acontecer, o finally vai ser executado
        session.close()