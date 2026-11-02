from flask import Blueprint

from app.services.espaco_service import EspacoService
from app.utils.decoradores import admin_obrigatorio, login_obrigatorio
from app.utils.requisicao import ler_json_obrigatorio, sucesso

espaco_bp = Blueprint("espacos", __name__, url_prefix="/api/espacos")
espaco_service = EspacoService()


@espaco_bp.get("")
@login_obrigatorio
def listar_espacos():
    espacos = espaco_service.listar_ativos()
    return sucesso([espaco.para_dicionario() for espaco in espacos])


@espaco_bp.get("/<int:id_espaco>")
@login_obrigatorio
def detalhar_espaco(id_espaco):
    return sucesso(espaco_service.buscar(id_espaco).para_dicionario())


@espaco_bp.post("")
@admin_obrigatorio
def cadastrar_espaco():
    espaco = espaco_service.cadastrar(ler_json_obrigatorio())
    return sucesso(espaco.para_dicionario(), "Espaço cadastrado com sucesso", 201)


@espaco_bp.put("/<int:id_espaco>")
@admin_obrigatorio
def editar_espaco(id_espaco):
    espaco = espaco_service.editar(id_espaco, ler_json_obrigatorio())
    return sucesso(espaco.para_dicionario(), "Espaço atualizado com sucesso")


@espaco_bp.post("/<int:id_espaco>/desativar")
@admin_obrigatorio
def desativar_espaco(id_espaco):
    espaco = espaco_service.desativar(id_espaco)
    return sucesso(espaco.para_dicionario(), "Espaço desativado com sucesso")
