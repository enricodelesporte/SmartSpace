from contextlib import contextmanager

import pymysql
from pymysql.cursors import DictCursor

from app.config import Configuracao


def abrir_conexao():
    return pymysql.connect(
        host=Configuracao.DB_HOST,
        port=Configuracao.DB_PORT,
        user=Configuracao.DB_USER,
        password=Configuracao.DB_PASSWORD,
        database=Configuracao.DB_NAME,
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=False,
        connect_timeout=5,
    )


@contextmanager
def transacao():
    conexao = abrir_conexao()
    try:
        yield conexao
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


def _com_conexao(conexao, operacao):
    if conexao is not None:
        return operacao(conexao)
    with transacao() as nova_conexao:
        return operacao(nova_conexao)


def consultar(sql, parametros=(), conexao=None):
    def operacao(cx):
        with cx.cursor() as cursor:
            cursor.execute(sql, parametros)
            return list(cursor.fetchall())

    return _com_conexao(conexao, operacao)


def consultar_um(sql, parametros=(), conexao=None):
    linhas = consultar(sql, parametros, conexao)
    return linhas[0] if linhas else None


def executar(sql, parametros=(), conexao=None):
    def operacao(cx):
        with cx.cursor() as cursor:
            cursor.execute(sql, parametros)
            return cursor.lastrowid

    return _com_conexao(conexao, operacao)


def testar_conexao():
    try:
        with transacao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT 1")
        return True, ""
    except pymysql.MySQLError as erro:
        return False, str(erro)
