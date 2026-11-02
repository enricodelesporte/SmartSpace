from datetime import date

from app.utils.apresentacao import (
    formatar_data_br,
    formatar_data_extenso,
    formatar_dia,
    formatar_dia_da_semana_abreviado,
    formatar_mes_abreviado,
    imagem_do_espaco,
    preparar_reserva_para_tela,
    separar_reservas,
)
from app.utils.texto import corrigir_texto_corrompido

HOJE = date(2026, 10, 25)


def reserva(data, status="CONFIRMADA", inicio="08:00", id_reserva=1):
    return {
        "id_reserva": id_reserva,
        "data_reserva": data,
        "hora_inicio": inicio,
        "hora_fim": "22:00",
        "status": status,
    }


def test_data_por_extenso_em_portugues():
    assert formatar_data_extenso("2026-12-05") == "sábado, 5 de dezembro de 2026"
    assert formatar_data_extenso(date(2026, 3, 2)) == "segunda-feira, 2 de março de 2026"


def test_partes_da_data_para_o_calendario():
    assert formatar_dia("2026-12-05") == "05"
    assert formatar_mes_abreviado("2026-12-05") == "dez"
    assert formatar_mes_abreviado("2026-03-02") == "mar"
    assert formatar_dia_da_semana_abreviado("2026-12-05") == "sáb"


def test_data_no_formato_brasileiro():
    assert formatar_data_br("2026-12-05") == "05/12/2026"


def test_imagem_do_espaco_ignora_acentos_e_maiusculas():
    assert imagem_do_espaco("Churrasqueira") == "img/churrasqueira.jpg"
    assert imagem_do_espaco("SALÃO DE FESTAS") == "img/salao.jpg"
    assert imagem_do_espaco("Sala de Jogos") is None


def test_reserva_futura_confirmada_pode_ser_cancelada():
    preparada = preparar_reserva_para_tela(reserva("2026-10-25"), HOJE)
    assert preparada["rotulo_status"] == "Confirmada"
    assert preparada["pode_cancelar"] is True


def test_reserva_passada_confirmada_vira_concluida_sem_cancelar():
    preparada = preparar_reserva_para_tela(reserva("2026-10-24"), HOJE)
    assert preparada["rotulo_status"] == "Concluída"
    assert preparada["pode_cancelar"] is False


def test_reserva_cancelada_nao_pode_ser_cancelada_de_novo():
    preparada = preparar_reserva_para_tela(reserva("2026-11-01", "CANCELADA"), HOJE)
    assert preparada["rotulo_status"] == "Cancelada"
    assert preparada["pode_cancelar"] is False


def test_separacao_em_proximas_e_historico_ordenadas():
    reservas = [
        reserva("2026-12-01", id_reserva=1),
        reserva("2026-11-01", id_reserva=2),
        reserva("2026-10-01", id_reserva=3),
        reserva("2026-11-15", "CANCELADA", id_reserva=4),
    ]
    proximas, historico = separar_reservas(reservas, HOJE)
    assert [r["id_reserva"] for r in proximas] == [2, 1]
    assert [r["id_reserva"] for r in historico] == [4, 3]


def test_corrige_texto_gravado_com_codificacao_errada():
    corrompido = "Salão de Festas".encode("utf-8").decode("cp850")
    assert "├" in corrompido
    assert corrigir_texto_corrompido(corrompido) == "Salão de Festas"
    corrompido = "Espaço para eventos e comemorações".encode("utf-8").decode("cp850")
    assert corrigir_texto_corrompido(corrompido) == "Espaço para eventos e comemorações"


def test_texto_correto_nao_e_alterado():
    assert corrigir_texto_corrompido("Salão de Festas") == "Salão de Festas"
    assert corrigir_texto_corrompido("Churrasqueira") == "Churrasqueira"
    assert corrigir_texto_corrompido(None) is None
    assert corrigir_texto_corrompido("") == ""
