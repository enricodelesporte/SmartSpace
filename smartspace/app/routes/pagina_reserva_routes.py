from datetime import date

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.services.espaco_service import EspacoService
from app.services.reserva_service import ReservaService
from app.utils.apresentacao import imagem_do_espaco, separar_reservas
from app.utils.decoradores import pagina_login_obrigatoria
from app.utils.excecoes import AppErro, ConflitoHorarioErro, ValidacaoErro
from app.utils.validadores import validar_data

pagina_reserva_bp = Blueprint("paginas_reservas", __name__)
espaco_service = EspacoService()
reserva_service = ReservaService()


def _data_escolhida(texto):
    if not texto:
        return date.today()
    try:
        return validar_data(texto, "data")
    except ValidacaoErro as erro:
        flash(erro.mensagem, "error")
        return date.today()


def _renderizar_reserva(espaco, data_texto):
    data_reserva = _data_escolhida(data_texto)
    opcoes = reserva_service.listar_opcoes_de_horario(espaco, data_reserva)
    opcao_padrao = next((o.id_opcao for o in opcoes if o.disponivel), None)
    return render_template(
        "reservar.html",
        espaco=espaco.para_dicionario(),
        imagem=imagem_do_espaco(espaco.nome),
        opcoes=opcoes,
        opcao_padrao=opcao_padrao,
        data_iso=data_reserva.isoformat(),
        hoje_iso=date.today().isoformat(),
    )


@pagina_reserva_bp.get("/espacos")
@pagina_login_obrigatoria
def espacos():
    itens = [
        {**espaco.para_dicionario(), "imagem": imagem_do_espaco(espaco.nome)}
        for espaco in espaco_service.listar_ativos()
    ]
    return render_template("espacos.html", espacos=itens)


@pagina_reserva_bp.route("/reservar/<int:id_espaco>", methods=["GET", "POST"])
@pagina_login_obrigatoria
def reservar(id_espaco):
    espaco = espaco_service.buscar(id_espaco)
    if not espaco.ativo:
        flash("Este espaço está desativado.", "error")
        return redirect(url_for("paginas_reservas.espacos"))
    if request.method == "POST":
        data_texto = request.form.get("data", "")
        try:
            reserva = reserva_service.reservar_opcao(
                g.usuario, espaco, data_texto, request.form.get("horario", "")
            )
        except ConflitoHorarioErro as erro:
            flash(erro.mensagem, "conflito")
            return _renderizar_reserva(espaco, data_texto)
        except AppErro as erro:
            flash(erro.mensagem, "error")
            return _renderizar_reserva(espaco, data_texto)
        return redirect(
            url_for("paginas_reservas.confirmada", id_reserva=reserva.id_reserva)
        )
    return _renderizar_reserva(espaco, request.args.get("data", ""))


@pagina_reserva_bp.get("/reserva-confirmada/<int:id_reserva>")
@pagina_login_obrigatoria
def confirmada(id_reserva):
    reserva = reserva_service.buscar_propria(g.usuario, id_reserva)
    return render_template("confirmacao.html", reserva=reserva.para_dicionario())


@pagina_reserva_bp.get("/minhas-reservas")
@pagina_login_obrigatoria
def minhas_reservas():
    reservas = reserva_service.listar_do_usuario(g.usuario)
    proximas, historico = separar_reservas(
        [reserva.para_dicionario() for reserva in reservas], date.today()
    )
    return render_template(
        "minhas_reservas.html", proximas=proximas, historico=historico
    )


@pagina_reserva_bp.post("/reservas/<int:id_reserva>/cancelar")
@pagina_login_obrigatoria
def cancelar(id_reserva):
    try:
        reserva_service.cancelar(g.usuario, id_reserva)
        flash("Reserva cancelada.", "success")
    except AppErro as erro:
        flash(erro.mensagem, "error")
    veio_do_admin = request.form.get("origem") == "admin"
    if veio_do_admin and g.usuario.pode_ver_todas_as_reservas():
        return redirect(url_for("paginas_admin.reservas_admin"))
    return redirect(url_for("paginas_reservas.minhas_reservas"))
