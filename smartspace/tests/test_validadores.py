from datetime import date, time, timedelta

import pytest

from app.utils.excecoes import ValidacaoErro
from app.utils.tempo import para_time
from app.utils.validadores import (
    validar_data,
    validar_data_nao_passada,
    validar_dados_espaco,
    validar_email,
    validar_hora,
    validar_inteiro_positivo,
    validar_intervalo_horario,
    validar_nome,
    validar_senha,
)


def test_nome_obrigatorio():
    with pytest.raises(ValidacaoErro):
        validar_nome("   ")
    with pytest.raises(ValidacaoErro):
        validar_nome(None)
    assert validar_nome("  Maria  ") == "Maria"


@pytest.mark.parametrize("email", ["", "semarroba", "a@b", "a@@b.com", "a b@c.com", None, 10])
def test_email_invalido(email):
    with pytest.raises(ValidacaoErro):
        validar_email(email)


def test_email_valido_e_normalizado():
    assert validar_email("  Maria@Exemplo.COM ") == "maria@exemplo.com"


def test_senha_minima_de_seis_caracteres():
    with pytest.raises(ValidacaoErro):
        validar_senha("12345")
    assert validar_senha("123456") == "123456"


def test_senha_muito_longa_para_bcrypt():
    with pytest.raises(ValidacaoErro):
        validar_senha("a" * 73)


@pytest.mark.parametrize("valor", ["abc", "", 0, -5, 3.5, True, None, "3.5", "-2", "\u00b2"])
def test_capacidade_invalida(valor):
    with pytest.raises(ValidacaoErro):
        validar_inteiro_positivo(valor, "capacidade_maxima")


@pytest.mark.parametrize("valor,esperado", [(10, 10), ("25", 25), (" 7 ", 7)])
def test_capacidade_valida(valor, esperado):
    assert validar_inteiro_positivo(valor, "capacidade_maxima") == esperado


def test_data_valida_e_invalida():
    assert validar_data("2026-11-20") == date(2026, 11, 20)
    for invalida in ["20/11/2026", "2026-13-01", "2026-02-30", "2026-1-5", "", None, 20261120]:
        with pytest.raises(ValidacaoErro):
            validar_data(invalida)


def test_hora_valida_e_invalida():
    assert validar_hora("08:30") == time(8, 30)
    for invalida in ["8:30", "25:00", "12:60", "12h", "", None]:
        with pytest.raises(ValidacaoErro):
            validar_hora(invalida)


def test_hora_fim_deve_ser_maior_que_inicio():
    validar_intervalo_horario(time(10, 0), time(11, 0))
    with pytest.raises(ValidacaoErro):
        validar_intervalo_horario(time(11, 0), time(11, 0))
    with pytest.raises(ValidacaoErro):
        validar_intervalo_horario(time(12, 0), time(11, 0))


def test_data_passada_bloqueada_e_hoje_permitido():
    hoje = date(2026, 11, 10)
    validar_data_nao_passada(hoje, hoje)
    validar_data_nao_passada(date(2026, 11, 11), hoje)
    with pytest.raises(ValidacaoErro):
        validar_data_nao_passada(date(2026, 11, 9), hoje)


def test_dados_de_espaco_validos():
    campos = validar_dados_espaco(
        {
            "nome": "Piscina",
            "capacidade_maxima": "15",
            "horario_abertura": "09:00",
            "horario_fechamento": "20:00",
        }
    )
    assert campos["capacidade_maxima"] == 15
    assert campos["descricao"] is None
    assert campos["horario_abertura"] == time(9, 0)


def test_dados_de_espaco_com_fechamento_antes_da_abertura():
    with pytest.raises(ValidacaoErro):
        validar_dados_espaco(
            {
                "nome": "Piscina",
                "capacidade_maxima": 15,
                "horario_abertura": "20:00",
                "horario_fechamento": "09:00",
            }
        )


def test_conversao_de_timedelta_do_mysql_para_time():
    assert para_time(timedelta(hours=8, minutes=30)) == time(8, 30)
    assert para_time(time(10, 0)) == time(10, 0)
