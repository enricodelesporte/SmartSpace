"""
Ponto único de acesso à conexão com o banco de dados PostgreSQL.

Mantido separado dos repositórios para que, se um dia trocarem de
psycopg2 para outra biblioteca (ex: SQLAlchemy), só este arquivo
precise mudar.
"""

import psycopg2
import psycopg2.extras

from app.config import Config


def get_connection():
    """
    Abre uma nova conexão com o PostgreSQL usando as credenciais do
    Config. `cursor_factory=RealDictCursor` faz cada linha do banco
    virar um dicionário (ex: row["nome"]), em vez de uma tupla
    posicional — deixa o código dos repositórios muito mais legível.
    """
    return psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        cursor_factory=psycopg2.extras.RealDictCursor,
    )
