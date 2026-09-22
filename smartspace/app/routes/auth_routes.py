"""
Rotas de autenticação: cadastro, login e logout.

Por enquanto expostas como uma pequena API JSON — fácil de testar
com curl/Postman antes de o front-end existir. Quando as telas HTML
forem montadas, estas mesmas funções podem passar a usar
render_template()/redirect() no lugar de jsonify(), sem mexer nos
services por baixo.
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request, session

from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
auth_service = AuthService()


@auth_bp.route("/cadastro", methods=["POST"])
def cadastro():
    """Fluxo 'Criar conta' do fluxograma."""
    dados = request.get_json(silent=True) or {}
    try:
        usuario = auth_service.registrar(
            nome=dados.get("nome", ""),
            email=dados.get("email", ""),
            senha=dados.get("senha", ""),
        )
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    return jsonify({"mensagem": "Conta criada com sucesso.", "usuario": _serializar(usuario)}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Fluxo 'Login' do fluxograma."""
    dados = request.get_json(silent=True) or {}
    try:
        usuario = auth_service.autenticar(
            email=dados.get("email", ""),
            senha=dados.get("senha", ""),
        )
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 401

    session["id_usuario"] = usuario.id_usuario
    return jsonify({"mensagem": "Login realizado com sucesso.", "usuario": _serializar(usuario)})


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensagem": "Sessão encerrada."})


def _serializar(usuario) -> dict:
    """Converte o objeto Usuario num dict simples para a resposta JSON."""
    return {
        "id_usuario": usuario.id_usuario,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo_usuario": usuario.tipo_usuario.value,
    }
