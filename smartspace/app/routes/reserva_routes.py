"""
Rotas de reserva: criar, listar (próprias ou todas) e cancelar.

O status HTTP 409 (Conflict) em `criar()` é proposital: combina
diretamente com o pop-up "Horário indisponível" desenhado no
protótipo de telas, então o front-end pode identificar esse caso
especificamente pelo código de status.
"""

from __future__ import annotations

from datetime import date, time

from flask import Blueprint, jsonify, request

from app.services.espaco_service import PermissaoNegadaError
from app.services.reserva_service import ConflitoDeHorarioError, ReservaService
from app.utils.decorators import login_required

reserva_bp = Blueprint("reserva", __name__, url_prefix="/reservas")
reserva_service = ReservaService()


@reserva_bp.route("", methods=["POST"])
@login_required
def criar(usuario):
    """Tela 'Fazer reserva' do morador."""
    dados = request.get_json(silent=True) or {}
    try:
        reserva = reserva_service.criar_reserva(
            morador=usuario,
            id_espaco=dados.get("id_espaco"),
            data_reserva=date.fromisoformat(dados.get("data_reserva", "")),
            hora_inicio=time.fromisoformat(dados.get("hora_inicio", "00:00")),
            hora_fim=time.fromisoformat(dados.get("hora_fim", "00:00")),
        )
    except ConflitoDeHorarioError as erro:
        return jsonify({"erro": str(erro)}), 409
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    return jsonify({"mensagem": "Reserva confirmada.", "reserva": _serializar(reserva)}), 201


@reserva_bp.route("/minhas", methods=["GET"])
@login_required
def minhas(usuario):
    """Tela 'Minhas Reservas' do morador."""
    reservas = reserva_service.listar_minhas_reservas(usuario)
    return jsonify([_serializar(r) for r in reservas])


@reserva_bp.route("", methods=["GET"])
@login_required
def todas(usuario):
    """Tela 'Todas as Reservas' do admin."""
    try:
        reservas = reserva_service.listar_todas(usuario)
    except PermissaoNegadaError as erro:
        return jsonify({"erro": str(erro)}), 403
    return jsonify([_serializar(r) for r in reservas])


@reserva_bp.route("/<int:id_reserva>/cancelar", methods=["POST"])
@login_required
def cancelar(usuario, id_reserva):
    """Botão 'Cancelar reserva', tanto do morador quanto do admin."""
    try:
        reserva_service.cancelar(usuario, id_reserva)
    except PermissaoNegadaError as erro:
        return jsonify({"erro": str(erro)}), 403
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 404

    return jsonify({"mensagem": "Reserva cancelada."})


def _serializar(reserva) -> dict:
    return {
        "id_reserva": reserva.id_reserva,
        "id_usuario": reserva.id_usuario,
        "id_espaco": reserva.id_espaco,
        "data_reserva": reserva.data_reserva.isoformat(),
        "hora_inicio": reserva.hora_inicio.strftime("%H:%M"),
        "hora_fim": reserva.hora_fim.strftime("%H:%M"),
        "status": reserva.status.value,
    }
