import sys

from app import create_app
from app.config import CAMINHO_ENV, Configuracao
from app.database import testar_conexao


def iniciar():
    print(f"Arquivo .env: {CAMINHO_ENV} (existe: {CAMINHO_ENV.exists()})")
    print(
        f"Conectando ao MySQL como usuário '{Configuracao.DB_USER}' "
        f"em {Configuracao.DB_HOST}:{Configuracao.DB_PORT}, banco '{Configuracao.DB_NAME}'"
    )
    conectou, mensagem = testar_conexao()
    if not conectou:
        print(f"FALHA NA CONEXÃO: {mensagem}")
        print("Confira DB_HOST, DB_PORT, DB_USER, DB_PASSWORD e DB_NAME no arquivo .env")
        sys.exit(1)
    print("Conexão com o banco OK")
    aplicacao = create_app()
    aplicacao.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    iniciar()
