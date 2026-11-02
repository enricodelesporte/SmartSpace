from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.services.auth_service import AuthService
from app.utils.decoradores import pagina_login_obrigatoria
from app.utils.excecoes import AppErro

pagina_conta_bp = Blueprint("paginas_conta", __name__)
auth_service = AuthService()


@pagina_conta_bp.get("/")
def inicio():
    if session.get("id_usuario"):
        return redirect(url_for("paginas_reservas.espacos"))
    return redirect(url_for("paginas_conta.login"))


@pagina_conta_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET" and session.get("id_usuario"):
        return redirect(url_for("paginas_reservas.espacos"))
    if request.method == "POST":
        email = request.form.get("email", "")
        try:
            usuario = auth_service.autenticar(
                {"email": email, "senha": request.form.get("senha", "")}
            )
        except AppErro as erro:
            flash(erro.mensagem, "error")
            return render_template("login.html", email=email)
        session.clear()
        session["id_usuario"] = usuario.id_usuario
        return redirect(url_for("paginas_reservas.espacos"))
    return render_template("login.html", email="")


@pagina_conta_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "")
        email = request.form.get("email", "")
        senha = request.form.get("senha", "")
        if senha != request.form.get("confirmar_senha", ""):
            flash("As senhas não conferem.", "error")
            return render_template("cadastro.html", nome=nome, email=email)
        try:
            auth_service.cadastrar_morador({"nome": nome, "email": email, "senha": senha})
        except AppErro as erro:
            flash(erro.mensagem, "error")
            return render_template("cadastro.html", nome=nome, email=email)
        flash("Conta criada com sucesso. Faça login para continuar.", "success")
        return redirect(url_for("paginas_conta.login"))
    return render_template("cadastro.html", nome="", email="")


@pagina_conta_bp.post("/logout")
def sair():
    session.clear()
    flash("Você saiu da conta.", "success")
    return redirect(url_for("paginas_conta.login"))


@pagina_conta_bp.route("/perfil", methods=["GET", "POST"])
@pagina_login_obrigatoria
def perfil():
    if request.method == "POST":
        dados = {"nome": request.form.get("nome", "")}
        nova_senha = request.form.get("senha", "")
        confirmacao = request.form.get("confirmar_senha", "")
        if nova_senha or confirmacao:
            if nova_senha != confirmacao:
                flash("As senhas não conferem.", "error")
                return render_template("perfil.html")
            dados["senha"] = nova_senha
        try:
            auth_service.atualizar_perfil(g.usuario, dados)
        except AppErro as erro:
            flash(erro.mensagem, "error")
            return render_template("perfil.html")
        flash("Perfil atualizado com sucesso.", "success")
        return redirect(url_for("paginas_conta.perfil"))
    return render_template("perfil.html")


@pagina_conta_bp.get("/configuracoes")
@pagina_login_obrigatoria
def configuracoes():
    return render_template("configuracoes.html")


@pagina_conta_bp.get("/sobre")
@pagina_login_obrigatoria
def sobre():
    return render_template("sobre.html")
