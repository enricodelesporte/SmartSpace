"""
Application factory do Flask.

Centraliza a criação da app e o registro dos blueprints de rotas —
padrão recomendado pela documentação oficial do Flask, e facilita
testes automatizados (cada teste pode criar sua própria instância
isolada, sem interferir em outra).
"""

from __future__ import annotations

from flask import Flask

from app.config import Config
from app.routes.auth_routes import auth_bp
from app.routes.espaco_routes import espaco_bp
from app.routes.reserva_routes import reserva_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(espaco_bp)
    app.register_blueprint(reserva_bp)

    @app.route("/")
    def index():
        return {"app": "SmartSpace", "status": "online"}

    return app
