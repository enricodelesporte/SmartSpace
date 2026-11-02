from datetime import date, time

from app.models.espaco import Espaco
from app.models.reserva import Reserva
from app.services.opcoes_horario import gerar_opcoes

DATA = date(2026, 12, 5)


def churrasqueira(abertura=time(8, 0), fechamento=time(22, 0)):
    return Espaco("Churrasqueira", None, 20, abertura, fechamento, id_espaco=1)


def salao():
    return Espaco("Salão de Festas", None, 50, time(8, 0), time(22, 0), id_espaco=2)


def reserva(id_espaco, inicio, fim, status=Reserva.CONFIRMADA):
    return Reserva(9, id_espaco, DATA, inicio, fim, status=status)


def ids_disponiveis(opcoes):
    return [o.id_opcao for o in opcoes if o.disponivel]


def test_churrasqueira_oferece_tres_horarios():
    opcoes = gerar_opcoes(churrasqueira(), [], DATA)
    assert [o.id_opcao for o in opcoes] == ["manha", "noite", "dia"]
    assert [o.rotulo for o in opcoes] == [
        "08:00 – 15:00",
        "16:00 – 22:00",
        "08:00 – 22:00",
    ]


def test_salao_oferece_apenas_o_dia_inteiro():
    opcoes = gerar_opcoes(salao(), [], DATA)
    assert [o.rotulo for o in opcoes] == ["08:00 – 22:00"]


def test_reserva_da_manha_bloqueia_manha_e_dia_mas_libera_noite():
    existentes = [reserva(1, time(8, 0), time(15, 0))]
    opcoes = gerar_opcoes(churrasqueira(), existentes, DATA)
    assert ids_disponiveis(opcoes) == ["noite"]


def test_reserva_cancelada_nao_bloqueia_opcoes():
    existentes = [reserva(1, time(8, 0), time(22, 0), status=Reserva.CANCELADA)]
    opcoes = gerar_opcoes(churrasqueira(), existentes, DATA)
    assert ids_disponiveis(opcoes) == ["manha", "noite", "dia"]


def test_reserva_de_outro_espaco_nao_bloqueia():
    existentes = [reserva(2, time(8, 0), time(22, 0))]
    assert ids_disponiveis(gerar_opcoes(churrasqueira(), existentes, DATA)) == [
        "manha",
        "noite",
        "dia",
    ]


def test_espaco_comum_usa_o_horario_de_funcionamento_como_dia_inteiro():
    sala = Espaco("Sala de Jogos", None, 12, time(9, 0), time(20, 0), id_espaco=3)
    opcoes = gerar_opcoes(sala, [], DATA)
    assert [(o.id_opcao, o.rotulo) for o in opcoes] == [("dia", "09:00 – 20:00")]


def test_horarios_fixos_que_nao_cabem_no_funcionamento_sao_descartados():
    opcoes = gerar_opcoes(churrasqueira(time(10, 0), time(23, 0)), [], DATA)
    assert [o.rotulo for o in opcoes] == ["16:00 – 22:00"]


def test_opcoes_tem_descricao_amigavel():
    opcoes = gerar_opcoes(churrasqueira(), [], DATA)
    assert [o.descricao for o in opcoes] == [
        "Manhã e almoço",
        "Final de tarde e noite",
        "Dia inteiro",
    ]
