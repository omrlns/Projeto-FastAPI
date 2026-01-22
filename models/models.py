from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

# conexão do branco de dados
db = create_engine("sqlite:///database/banco.db")

# base do banco de dados
Base = declarative_base()

# classes/tabelas do banco
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    perfilAtivo = Column("perfilAtivo", Boolean)
    perfilAdmin = Column("perfilAdmin", Boolean, default=False)

    def __init__(self, nome, email, senha, perfilAtivo=True, perfilAdmin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.perfilAtivo = perfilAtivo
        self.perfilAdmin = perfilAdmin
        

class Pedido(Base):
    __tablename__ = "pedidos"

    STATUS_PEDIDOS = [("PENDENTE", "PENDENTE"), ("CANCELADO", "CANCELADO"), ("FINALIZADO", "FINALIZADO")]

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", ChoiceType(choices=STATUS_PEDIDOS)) # PENDENTE, CANCELADO, FINALIZADO
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    # itens

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status

# ItensPedido

# execução e criação dos metadados do seu banco (cria efetivamente o banco de dados)
