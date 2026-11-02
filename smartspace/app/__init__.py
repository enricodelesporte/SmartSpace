from flask import Flask, g, request


def create_app():
    from app.config import Configuracao
    from app.routes.api_status_routes import api_status_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.espaco_routes import espaco_bp
    from app.routes.pagina_admin_routes import pagina_admin_bp
    from app.routes.pagina_conta_routes import pagina_conta_bp
    from app.routes.pagina_reserva_routes import pagina_reserva_bp
    from app.routes.reserva_routes import reserva_bp
    from app.tratadores_erro import registrar_tratadores_de_erro
    from app.utils.apresentacao import (
        VALOR_RESERVA,
        formatar_data_br,
        formatar_data_extenso,
        formatar_dia,
        formatar_dia_da_semana_abreviado,
        formatar_mes_abreviado,
        formatar_status,
    )
    from app.utils.csrf import obter_token_csrf, validar_token_csrf

    if not Configuracao.SECRET_KEY:
        raise RuntimeError("SECRET_KEY não definida no arquivo .env")

    app = Flask(__name__)
    app.config.from_object(Configuracao)
    app.json.ensure_ascii = False

    app.register_blueprint(api_status_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(espaco_bp)
    app.register_blueprint(reserva_bp)
    app.register_blueprint(pagina_conta_bp)
    app.register_blueprint(pagina_reserva_bp)
    app.register_blueprint(pagina_admin_bp)

    app.add_template_filter(formatar_data_br, "data_br")
    app.add_template_filter(formatar_status, "status_br")
    app.add_template_filter(formatar_data_extenso, "data_extenso")
    app.add_template_filter(formatar_dia, "dia")
    app.add_template_filter(formatar_mes_abreviado, "mes_abreviado")
    app.add_template_filter(formatar_dia_da_semana_abreviado, "dia_da_semana")

    @app.before_request
    def proteger_formularios_das_paginas():
        rota_existe = request.endpoint is not None
        if rota_existe and request.method == "POST" and not request.path.startswith("/api"):
            validar_token_csrf()

    @app.context_processor
    def injetar_contexto_dos_templates():
        return {
            "app_name": "SmartSpace",
            "usuario": g.get("usuario"),
            "csrf_token": obter_token_csrf,
            "valor_reserva": VALOR_RESERVA,
        }

    registrar_tratadores_de_erro(app)
    return app
