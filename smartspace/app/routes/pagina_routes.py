from flask import Blueprint, jsonify, render_template

pagina_bp = Blueprint("paginas", __name__)


@pagina_bp.get("/")
def status_aplicacao():
    return jsonify({"aplicacao": "SmartSpace", "status": "online"})


@pagina_bp.get("/app/login")
def pagina_login():
    return render_template("login.html")


@pagina_bp.get("/app/cadastro")
def pagina_cadastro():
    return render_template("cadastro.html")


@pagina_bp.get("/app/espacos")
def pagina_espacos():
    return render_template("espacos.html")


@pagina_bp.get("/app/minhas-reservas")
def pagina_minhas_reservas():
    return render_template("minhas_reservas.html")


@pagina_bp.get("/app/perfil")
def pagina_perfil():
    return render_template("perfil.html")


@pagina_bp.get("/app/admin/espacos")
def pagina_admin_espacos():
    return render_template("admin_espacos.html")


@pagina_bp.get("/app/admin/reservas")
def pagina_admin_reservas():
    return render_template("admin_reservas.html")
