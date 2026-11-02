import logging

import pymysql
from flask import flash, jsonify, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException

from app.utils.excecoes import AppErro

registro_log = logging.getLogger("smartspace")


def _requisicao_da_api():
    return request.path.startswith("/api")


def _responder_erro(mensagem, codigo_http):
    if _requisicao_da_api():
        return jsonify({"erro": mensagem}), codigo_http
    if codigo_http == 401:
        flash(mensagem, "error")
        return redirect(url_for("paginas_conta.login"))
    return render_template("erro.html", codigo=codigo_http, mensagem=mensagem), codigo_http


def registrar_tratadores_de_erro(app):
    @app.errorhandler(AppErro)
    def tratar_erro_da_aplicacao(erro):
        return _responder_erro(erro.mensagem, erro.codigo_http)

    @app.errorhandler(HTTPException)
    def tratar_erro_http(erro):
        return _responder_erro(erro.description, erro.code)

    @app.errorhandler(pymysql.MySQLError)
    def tratar_erro_de_banco(erro):
        registro_log.exception("Erro de banco de dados")
        return _responder_erro("Banco de dados indisponível ou com erro", 503)

    @app.errorhandler(Exception)
    def tratar_erro_inesperado(erro):
        registro_log.exception("Erro inesperado")
        return _responder_erro("Erro interno do servidor", 500)
