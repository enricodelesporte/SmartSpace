from datetime import date, time

from app.models.espaco import Espaco
from app.models.reserva import Reserva

DATA = date(2026, 11, 20)


def criar_espaco():
    return Espaco("Salão de Festas", None, 50, time(8, 0), time(22, 0), id_espaco=1)


def criar_reserva(inicio, fim, id_espaco=1, data=DATA, status=Reserva.CONFIRMADA):
    return Reserva(1, id_espaco, data, inicio, fim, status=status)


def test_intervalos_que_se_sobrepoem_geram_conflito():
    existente = criar_reserva(time(18, 0), time(21, 0))
    nova = criar_reserva(time(20, 0), time(22, 0))
    assert not criar_espaco().esta_disponivel(nova, [existente])


def test_nova_reserva_contida_em_outra_gera_conflito():
    existente = criar_reserva(time(10, 0), time(18, 0))
    nova = criar_reserva(time(12, 0), time(13, 0))
    assert not criar_espaco().esta_disponivel(nova, [existente])


def test_nova_reserva_que_engloba_outra_gera_conflito():
    existente = criar_reserva(time(12, 0), time(13, 0))
    nova = criar_reserva(time(10, 0), time(18, 0))
    assert not criar_espaco().esta_disponivel(nova, [existente])


def test_horarios_consecutivos_sao_permitidos():
    existente = criar_reserva(time(19, 0), time(21, 0))
    nova = criar_reserva(time(21, 0), time(23, 0))
    assert criar_espaco().esta_disponivel(nova, [existente])
    assert criar_espaco().esta_disponivel(existente, [nova])


def test_reserva_cancelada_nao_conta_para_conflito():
    cancelada = criar_reserva(time(18, 0), time(21, 0), status=Reserva.CANCELADA)
    nova = criar_reserva(time(18, 0), time(21, 0))
    assert criar_espaco().esta_disponivel(nova, [cancelada])


def test_reservas_em_datas_diferentes_nao_conflitam():
    existente = criar_reserva(time(18, 0), time(21, 0))
    nova = criar_reserva(time(18, 0), time(21, 0), data=date(2026, 11, 21))
    assert criar_espaco().esta_disponivel(nova, [existente])


def test_reservas_em_espacos_diferentes_nao_conflitam():
    existente = criar_reserva(time(18, 0), time(21, 0), id_espaco=2)
    nova = criar_reserva(time(18, 0), time(21, 0), id_espaco=1)
    assert criar_espaco().esta_disponivel(nova, [existente])


def test_horario_dentro_do_funcionamento_do_espaco():
    espaco = criar_espaco()
    assert espaco.comporta_horario(time(8, 0), time(22, 0))
    assert not espaco.comporta_horario(time(7, 0), time(10, 0))
    assert not espaco.comporta_horario(time(20, 0), time(23, 0))
