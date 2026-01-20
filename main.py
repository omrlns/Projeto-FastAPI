from fastapi import FastAPI

app = FastAPI()
# para rodar a api, deve-se executar no terminal: uvicorn main:app --reload

from routes.autenticacao import autenticacao_router
from routes.pedidos import pedidos_router

app.include_router(autenticacao_router)
app.include_router(pedidos_router)
