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

    # STATUS_PEDIDOS = [("PENDENTE", "PENDENTE"), ("CANCELADO", "CANCELADO"), ("FINALIZADO", "FINALIZADO")]

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) # PENDENTE, CANCELADO, FINALIZADO
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    # itens

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status

# ItensPedido
class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido



# execução e criação dos metadados do seu banco (cria efetivamente o banco de dados)
