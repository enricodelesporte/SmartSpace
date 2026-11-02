import sys
from getpass import getpass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import Configuracao
from app.database import testar_conexao
from app.services.auth_service import AuthService
from app.utils.excecoes import AppErro


def criar_admin_pelo_terminal():
    conectou, mensagem = testar_conexao()
    if not conectou:
        print(
            f"Falha na conexão ({Configuracao.DB_USER}@{Configuracao.DB_HOST}"
            f"/{Configuracao.DB_NAME}): {mensagem}"
        )
        sys.exit(1)
    nome = input("Nome do administrador: ")
    email = input("E-mail: ")
    senha = getpass("Senha (mínimo 6 caracteres): ")
    confirmacao = getpass("Confirme a senha: ")
    if senha != confirmacao:
        print("As senhas não conferem")
        sys.exit(1)
    try:
        admin = AuthService().criar_admin(nome, email, senha)
    except AppErro as erro:
        print(f"Erro: {erro.mensagem}")
        sys.exit(1)
    print(f"Administrador criado: {admin.nome} ({admin.email})")


if __name__ == "__main__":
    criar_admin_pelo_terminal()
