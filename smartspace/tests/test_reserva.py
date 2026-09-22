"""
Testes unitários da regra de conflito de horário (Reserva.sobrepoe).

Não dependem de banco de dados — testam só a lógica de domínio, que
é a parte mais importante de saber explicar na avaliação individual.

Rode com: pytest
"""

from datetime import date, time

from app.models.reserva import Reserva, StatusReserva


def _reserva(hora_inicio: time, hora_fim: time, status: StatusReserva = StatusReserva.CONFIRMADA) -> Reserva:
    return Reserva(
        id_reserva=1,
        id_usuario=1,
        id_espaco=1,
        data_reserva=date(2026, 9, 20),
        hora_inicio=hora_inicio,
        hora_fim=hora_fim,
        status=status,
    )


def test_horarios_sobrepostos_devem_conflitar():
    r1 = _reserva(time(19, 0), time(21, 0))
    r2 = _reserva(time(20, 0), time(22, 0))
    assert r1.sobrepoe(r2) is True


def test_horarios_consecutivos_nao_devem_conflitar():
    """19h-21h e 21h-23h não se sobrepõem: um termina exatamente quando o outro começa."""
    r1 = _reserva(time(19, 0), time(21, 0))
    r2 = _reserva(time(21, 0), time(23, 0))
    assert r1.sobrepoe(r2) is False


def test_reserva_cancelada_nao_conta_como_conflito():
    r1 = _reserva(time(19, 0), time(21, 0))
    r2 = _reserva(time(19, 0), time(21, 0), status=StatusReserva.CANCELADA)
    assert r1.sobrepoe(r2) is False


def test_espacos_diferentes_nao_conflitam_mesmo_com_mesmo_horario():
    r1 = _reserva(time(19, 0), time(21, 0))
    r2 = _reserva(time(19, 0), time(21, 0))
    r2.id_espaco = 2
    assert r1.sobrepoe(r2) is False
