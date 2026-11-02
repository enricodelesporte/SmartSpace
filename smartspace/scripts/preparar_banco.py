import sys
from pathlib import Path

RAIZ_DO_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ_DO_PROJETO))

import pymysql

from app.config import CAMINHO_ENV, Configuracao
from app.utils.texto import corrigir_texto_corrompido

CAMINHO_SCHEMA = RAIZ_DO_PROJETO / "database" / "schema_mysql.sql"
COLUNAS_DE_TEXTO = (
    ("espaco", "id_espaco", ("nome", "descricao")),
    ("usuario", "id_usuario", ("nome",)),
)


def separar_comandos(script):
    return [comando.strip() for comando in script.split(";") if comando.strip()]


def comando_de_banco_ou_uso(comando):
    inicio = comando.upper()
    return inicio.startswith("CREATE DATABASE") or inicio.startswith("USE ")


def comando_de_dados(comando):
    return comando.upper().startswith("INSERT")


def conectar_ao_servidor():
    return pymysql.connect(
        host=Configuracao.DB_HOST,
        port=Configuracao.DB_PORT,
        user=Configuracao.DB_USER,
        password=Configuracao.DB_PASSWORD,
        charset="utf8mb4",
        connect_timeout=5,
    )


def executar_comandos(conexao, comandos):
    with conexao.cursor() as cursor:
        for comando in comandos:
            cursor.execute(comando)
    conexao.commit()


def criar_banco(conexao):
    with conexao.cursor() as cursor:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{Configuracao.DB_NAME}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
    conexao.select_db(Configuracao.DB_NAME)


def ler_comandos_do_schema():
    script = CAMINHO_SCHEMA.read_text(encoding="utf-8")
    return [
        comando
        for comando in separar_comandos(script)
        if not comando_de_banco_ou_uso(comando)
    ]


def reparar_textos_corrompidos(conexao):
    corrigidos = 0
    with conexao.cursor() as cursor:
        for tabela, chave, colunas in COLUNAS_DE_TEXTO:
            cursor.execute(f"SELECT {chave}, {', '.join(colunas)} FROM {tabela}")
            for linha in cursor.fetchall():
                identificador, valores = linha[0], list(linha[1:])
                novos_valores = [corrigir_texto_corrompido(valor) for valor in valores]
                if valores != novos_valores:
                    atribuicoes = ", ".join(f"{coluna} = %s" for coluna in colunas)
                    cursor.execute(
                        f"UPDATE {tabela} SET {atribuicoes} WHERE {chave} = %s",
                        (*novos_valores, identificador),
                    )
                    corrigidos += 1
    conexao.commit()
    return corrigidos


def listar_espacos(conexao):
    with conexao.cursor() as cursor:
        cursor.execute(
            "SELECT nome, descricao, horario_abertura, horario_fechamento "
            "FROM espaco ORDER BY id_espaco"
        )
        return cursor.fetchall()


def preparar_banco():
    print(f"Arquivo .env: {CAMINHO_ENV} (existe: {CAMINHO_ENV.exists()})")
    print(
        f"Conectando como '{Configuracao.DB_USER}' em "
        f"{Configuracao.DB_HOST}:{Configuracao.DB_PORT}, banco '{Configuracao.DB_NAME}'"
    )
    try:
        conexao = conectar_ao_servidor()
    except pymysql.MySQLError as erro:
        print(f"FALHA NA CONEXÃO: {erro}")
        print("Confira DB_HOST, DB_PORT, DB_USER e DB_PASSWORD no arquivo .env")
        sys.exit(1)
    try:
        criar_banco(conexao)
        comandos = ler_comandos_do_schema()
        executar_comandos(
            conexao, [c for c in comandos if not comando_de_dados(c)]
        )
        corrigidos = reparar_textos_corrompidos(conexao)
        executar_comandos(conexao, [c for c in comandos if comando_de_dados(c)])
        espacos = listar_espacos(conexao)
    finally:
        conexao.close()
    print("Banco e tabelas prontos.")
    print(f"Registros com acentuação corrigida: {corrigidos}")
    print("Espaços cadastrados:")
    for nome, descricao, abertura, fechamento in espacos:
        print(f"  - {nome} | {descricao} | {abertura} às {fechamento}")


if __name__ == "__main__":
    preparar_banco()
