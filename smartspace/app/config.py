"""
Configurações centrais da aplicação.

Tudo que muda entre ambientes (senha de banco, chave secreta etc.)
vem de variáveis de ambiente, nunca hardcoded no código — boa
prática de Engenharia de Software e evita vazar credenciais se o
repositório for público.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuração única da aplicação, lida do arquivo .env (ver .env.example)."""

    SECRET_KEY = os.getenv("SECRET_KEY", "chave-temporaria-trocar-em-producao")

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "smartspace")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
