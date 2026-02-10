from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES =  int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()
# para rodar a api, deve-se executar no terminal: uvicorn main:app --reload

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="autenticacao/login")

from routes.autenticacao import autenticacao_router
from routes.pedidos import pedidos_router

app.include_router(autenticacao_router)
app.include_router(pedidos_router)
