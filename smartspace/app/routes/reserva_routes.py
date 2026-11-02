from flask import Blueprint, g, request

from app.services.reserva_service import ReservaService
from app.utils.decoradores import login_obrigatorio
from app.utils.requisicao import ler_json_obrigatorio, sucesso
from app.utils.validadores import validar_data, validar_inteiro_positivo

reserva_bp = Blueprint("reservas", __name__, url_prefix="/api/reservas")
reserva_service = ReservaService()


@reserva_bp.post("")
@login_obrigatorio
def criar_reserva():
    reserva = reserva_service.criar(g.usuario, ler_json_obrigatorio())
    return sucesso(reserva.para_dicionario(), "Reserva confirmada com sucesso", 201)


@reserva_bp.get("/minhas")
@login_obrigatorio
def listar_minhas_reservas():
    reservas = reserva_service.listar_do_usuario(g.usuario)
    return sucesso([reserva.para_dicionario() for reserva in reservas])


@reserva_bp.get("")
@login_obrigatorio
def listar_todas_as_reservas():
    id_espaco_texto = request.args.get("id_espaco")
    data_texto = request.args.get("data")
    id_espaco = (
        validar_inteiro_positivo(id_espaco_texto, "id_espaco")
        if id_espaco_texto
        else None
    )
    data_reserva = validar_data(data_texto, "data") if data_texto else None
    reservas = reserva_service.listar_todas(g.usuario, id_espaco, data_reserva)
    return sucesso([reserva.para_dicionario() for reserva in reservas])


@reserva_bp.post("/<int:id_reserva>/cancelar")
@login_obrigatorio
def cancelar_reserva(id_reserva):
    reserva = reserva_service.cancelar(g.usuario, id_reserva)
    return sucesso(reserva.para_dicionario(), "Reserva cancelada com sucesso")
