from flask import jsonify, request

from app.utils.excecoes import ValidacaoErro


def ler_json_obrigatorio():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        raise ValidacaoErro("Corpo da requisição deve ser um JSON válido (objeto)")
    return dados


def sucesso(dados=None, mensagem=None, codigo_http=200):
    corpo = {}
    if mensagem is not None:
        corpo["mensagem"] = mensagem
    if dados is not None:
        corpo["dados"] = dados
    return jsonify(corpo), codigo_http
