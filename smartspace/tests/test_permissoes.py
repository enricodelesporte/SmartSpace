from datetime import date, time

import pytest

from app.models.reserva import Reserva
from app.models.usuario import Admin, Morador, UsuarioFactory
from app.utils.excecoes import ValidacaoErro


def reserva_do_usuario(id_usuario):
    return Reserva(id_usuario, 1, date(2026, 11, 20), time(10, 0), time(12, 0))


def test_morador_nao_gerencia_espacos_nem_ve_todas_as_reservas():
    morador = Morador("Enrico", "e@x.com", "hash", id_usuario=2)
    assert not morador.pode_gerenciar_espacos()
    assert not morador.pode_ver_todas_as_reservas()


def test_admin_gerencia_espacos_e_ve_todas_as_reservas():
    admin = Admin("Maria", "m@x.com", "hash", id_usuario=1)
    assert admin.pode_gerenciar_espacos()
    assert admin.pode_ver_todas_as_reservas()


def test_morador_cancela_apenas_a_propria_reserva():
    morador = Morador("Enrico", "e@x.com", "hash", id_usuario=2)
    assert morador.pode_cancelar_reserva(reserva_do_usuario(2))
    assert not morador.pode_cancelar_reserva(reserva_do_usuario(3))


def test_admin_cancela_qualquer_reserva():
    admin = Admin("Maria", "m@x.com", "hash", id_usuario=1)
    assert admin.pode_cancelar_reserva(reserva_do_usuario(2))


def test_factory_cria_a_subclasse_correta():
    assert isinstance(UsuarioFactory.criar("ADMIN", "A", "a@x.com", "h"), Admin)
    assert isinstance(UsuarioFactory.criar("MORADOR", "B", "b@x.com", "h"), Morador)
    with pytest.raises(ValidacaoErro):
        UsuarioFactory.criar("VISITANTE", "C", "c@x.com", "h")


def test_dicionario_do_usuario_nao_expoe_o_hash_da_senha():
    morador = Morador("Enrico", "e@x.com", "segredo", id_usuario=2)
    assert "senha_hash" not in morador.para_dicionario()
    assert morador.para_dicionario()["tipo_usuario"] == "MORADOR"


def test_nao_cancela_reserva_ja_cancelada():
    reserva = reserva_do_usuario(2)
    reserva.cancelar()
    with pytest.raises(ValidacaoErro):
        reserva.cancelar()
