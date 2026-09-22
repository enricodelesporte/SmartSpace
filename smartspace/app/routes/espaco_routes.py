"""
Rotas de espaços: listar (qualquer usuário logado) e
cadastrar/desativar (somente Admin — checado pelo decorator
admin_required).
"""

from __future__ import annotations

from datetime import time

from flask import Blueprint, jsonify, request

from app.services.espaco_service import EspacoService, PermissaoNegadaError
from app.utils.decorators import admin_required, login_required

espaco_bp = Blueprint("espaco", __name__, url_prefix="/espacos")
espaco_service = EspacoService()


@espaco_bp.route("", methods=["GET"])
@login_required
def listar(usuario):
    """Tela 'Espaços disponíveis' do morador."""
    espacos = espaco_service.listar_disponiveis()
    return jsonify([_serializar(e) for e in espacos])


@espaco_bp.route("", methods=["POST"])
@admin_required
def cadastrar(usuario):
    """Tela 'Cadastrar espaço' do admin."""
    dados = request.get_json(silent=True) or {}
    try:
        espaco = espaco_service.cadastrar(
            solicitante=usuario,
            nome=dados.get("nome", ""),
            descricao=dados.get("descricao"),
            capacidade_maxima=dados.get("capacidade_maxima"),
            horario_abertura=time.fromisoformat(dados.get("horario_abertura", "00:00")),
            horario_fechamento=time.fromisoformat(dados.get("horario_fechamento", "00:00")),
        )
    except (ValueError, PermissaoNegadaError) as erro:
        return jsonify({"erro": str(erro)}), 400

    return jsonify({"mensagem": "Espaço cadastrado.", "espaco": _serializar(espaco)}), 201


@espaco_bp.route("/<int:id_espaco>/desativar", methods=["POST"])
@admin_required
def desativar(usuario, id_espaco):
    """Tela 'Gerenciar espaços' do admin — botão Desativar."""
    try:
        espaco_service.desativar(usuario, id_espaco)
    except PermissaoNegadaError as erro:
        return jsonify({"erro": str(erro)}), 403

    return jsonify({"mensagem": "Espaço desativado."})


def _serializar(espaco) -> dict:
    return {
        "id_espaco": espaco.id_espaco,
        "nome": espaco.nome,
        "descricao": espaco.descricao,
        "capacidade_maxima": espaco.capacidade_maxima,
        "horario_abertura": espaco.horario_abertura.strftime("%H:%M"),
        "horario_fechamento": espaco.horario_fechamento.strftime("%H:%M"),
        "ativo": espaco.ativo,
    }
