"""
Decorators de controle de acesso para as rotas Flask.

Centraliza a checagem de "está logado?" e "é admin?" pra não
repetir esse código em cada rota — atende o requisito 9 (perfis de
usuário com permissões distintas) na camada de rotas.
"""

from __future__ import annotations

from functools import wraps

from flask import jsonify, session

from app.repositories.usuario_repository import UsuarioRepository


def usuario_logado():
    """Recupera o usuário da sessão atual, ou None se ninguém estiver logado."""
    id_usuario = session.get("id_usuario")
    if id_usuario is None:
        return None
    return UsuarioRepository().buscar_por_id(id_usuario)


def login_required(func):
    """Bloqueia a rota se não houver usuário logado na sessão."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        usuario = usuario_logado()
        if usuario is None:
            return jsonify({"erro": "É necessário estar autenticado."}), 401
        return func(usuario, *args, **kwargs)

    return wrapper


def admin_required(func):
    """Bloqueia a rota se o usuário logado não for Admin."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        usuario = usuario_logado()
        if usuario is None:
            return jsonify({"erro": "É necessário estar autenticado."}), 401
        if not usuario.pode_gerenciar_espacos():
            return jsonify({"erro": "Acesso restrito a administradores."}), 403
        return func(usuario, *args, **kwargs)

    return wrapper
