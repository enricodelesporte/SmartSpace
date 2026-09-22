"""
Funções de hash e verificação de senha, usando bcrypt.

Regra de ouro: senha NUNCA é armazenada nem comparada em texto
puro — só o hash (requisito 7: autenticação de usuário, feita de
forma segura).
"""

import bcrypt


def gerar_hash_senha(senha: str) -> str:
    """Gera o hash a partir da senha em texto puro (usado no cadastro)."""
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Compara a senha digitada no login com o hash salvo no banco."""
    return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))
