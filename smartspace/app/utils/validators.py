"""
Validações reutilizáveis de entrada de dados.

Atende diretamente o requisito 4 do roteiro ("Validação de Dados —
verificações que evitem erros, ex.: impedir texto em campo
numérico"). Centralizar aqui evita duplicar a mesma checagem em
vários lugares do código.
"""

import re
from datetime import time

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_email(email: str) -> bool:
    """Formato básico de e-mail (usuario@dominio.com)."""
    return bool(email) and bool(EMAIL_REGEX.match(email))


def validar_senha(senha: str, minimo: int = 6) -> bool:
    """Regra mínima de senha: pelo menos `minimo` caracteres."""
    return bool(senha) and len(senha) >= minimo


def validar_capacidade(valor) -> int:
    """
    Garante que a capacidade é um número inteiro positivo — impede
    que texto seja aceito num campo que deveria ser numérico
    (exemplo citado literalmente no roteiro do projeto).
    """
    try:
        capacidade = int(valor)
    except (TypeError, ValueError):
        raise ValueError("Capacidade deve ser um número inteiro.")
    if capacidade <= 0:
        raise ValueError("Capacidade deve ser maior que zero.")
    return capacidade


def validar_horario(hora_inicio: time, hora_fim: time) -> None:
    """Garante que o horário final é depois do horário inicial."""
    if hora_fim <= hora_inicio:
        raise ValueError("O horário de término deve ser depois do horário de início.")
