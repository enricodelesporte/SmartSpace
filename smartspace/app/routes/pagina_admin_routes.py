from datetime import date

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.services.espaco_service import EspacoService
from app.services.reserva_service import ReservaService
from app.utils.apresentacao import imagem_do_espaco, preparar_reserva_para_tela
from app.utils.decoradores import pagina_admin_obrigatoria
from app.utils.excecoes import AppErro, ValidacaoErro
from app.utils.validadores import validar_data, validar_inteiro_positivo

pagina_admin_bp = Blueprint("paginas_admin", __name__, url_prefix="/admin")
espaco_service = EspacoService()
reserva_service = ReservaService()


def _dados_do_formulario_de_espaco():
    return {
        "nome": request.form.get("nome", ""),
        "descricao": request.form.get("descricao", ""),
        "capacidade_maxima": request.form.get("capacidade_maxima", ""),
        "horario_abertura": request.form.get("horario_abertura", ""),
        "horario_fechamento": request.form.get("horario_fechamento", ""),
    }


@pagina_admin_bp.get("/espacos")
@pagina_admin_obrigatoria
def espacos_admin():
    itens = [
        {**espaco.para_dicionario(), "imagem": imagem_do_espaco(espaco.nome)}
        for espaco in espaco_service.listar_ativos()
    ]
    return render_template("admin_espacos.html", espacos=itens)


@pagina_admin_bp.route("/espacos/novo", methods=["GET", "POST"])
@pagina_admin_obrigatoria
def novo_espaco():
    if request.method == "POST":
        dados = _dados_do_formulario_de_espaco()
        try:
            espaco_service.cadastrar(dados)
        except AppErro as erro:
            flash(erro.mensagem, "error")
            return render_template("admin_espaco_form.html", espaco=dados, editando=False)
        flash("Espaço cadastrado com sucesso.", "success")
        return redirect(url_for("paginas_admin.espacos_admin"))
    return render_template(
        "admin_espaco_form.html",
        espaco={
            "nome": "",
            "descricao": "",
            "capacidade_maxima": "",
            "horario_abertura": "08:00",
            "horario_fechamento": "22:00",
        },
        editando=False,
    )


@pagina_admin_bp.route("/espacos/<int:id_espaco>/editar", methods=["GET", "POST"])
@pagina_admin_obrigatoria
def editar_espaco(id_espaco):
    espaco = espaco_service.buscar(id_espaco)
    if request.method == "POST":
        dados = {**_dados_do_formulario_de_espaco(), "id_espaco": id_espaco}
        try:
            espaco_service.editar(id_espaco, dados)
        except AppErro as erro:
            flash(erro.mensagem, "error")
            return render_template("admin_espaco_form.html", espaco=dados, editando=True)
        flash("Espaço atualizado com sucesso.", "success")
        return redirect(url_for("paginas_admin.espacos_admin"))
    return render_template(
        "admin_espaco_form.html", espaco=espaco.para_dicionario(), editando=True
    )


@pagina_admin_bp.post("/espacos/<int:id_espaco>/desativar")
@pagina_admin_obrigatoria
def desativar_espaco(id_espaco):
    try:
        espaco_service.desativar(id_espaco)
        flash("Espaço desativado. As reservas existentes foram mantidas.", "success")
    except AppErro as erro:
        flash(erro.mensagem, "error")
    return redirect(url_for("paginas_admin.espacos_admin"))


@pagina_admin_bp.get("/reservas")
@pagina_admin_obrigatoria
def reservas_admin():
    id_espaco_texto = request.args.get("id_espaco", "")
    data_texto = request.args.get("data", "")
    id_espaco = None
    data_reserva = None
    try:
        if id_espaco_texto:
            id_espaco = validar_inteiro_positivo(id_espaco_texto, "espaço")
        if data_texto:
            data_reserva = validar_data(data_texto, "data")
    except ValidacaoErro as erro:
        flash(erro.mensagem, "error")
        id_espaco = None
        data_reserva = None
    reservas = reserva_service.listar_todas(g.usuario, id_espaco, data_reserva)
    return render_template(
        "admin_reservas.html",
        reservas=[
            preparar_reserva_para_tela(reserva.para_dicionario(), date.today())
            for reserva in reservas
        ],
        espacos=[espaco.para_dicionario() for espaco in espaco_service.listar_ativos()],
        filtro_espaco=id_espaco,
        filtro_data=data_reserva.isoformat() if data_reserva else "",
    )
