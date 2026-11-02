import unicodedata
from datetime import date

VALOR_RESERVA = "R$ 80,00"
IMAGEM_CHURRASQUEIRA = "img/churrasqueira.jpg"
IMAGEM_SALAO = "img/salao.jpg"

DIAS_DA_SEMANA = (
    "segunda-feira",
    "terça-feira",
    "quarta-feira",
    "quinta-feira",
    "sexta-feira",
    "sábado",
    "domingo",
)
MESES = (
    "janeiro",
    "fevereiro",
    "março",
    "abril",
    "maio",
    "junho",
    "julho",
    "agosto",
    "setembro",
    "outubro",
    "novembro",
    "dezembro",
)


def normalizar_texto(texto):
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore")
    return sem_acento.decode("ascii").lower()


def imagem_do_espaco(nome):
    nome_normalizado = normalizar_texto(nome)
    if "churrasq" in nome_normalizado:
        return IMAGEM_CHURRASQUEIRA
    if "salao" in nome_normalizado or "festa" in nome_normalizado:
        return IMAGEM_SALAO
    return None


def _como_data(valor):
    if isinstance(valor, str):
        return date.fromisoformat(valor)
    return valor


def formatar_data_br(valor):
    return _como_data(valor).strftime("%d/%m/%Y")


def formatar_data_extenso(valor):
    data = _como_data(valor)
    return (
        f"{DIAS_DA_SEMANA[data.weekday()]}, {data.day} de "
        f"{MESES[data.month - 1]} de {data.year}"
    )


def formatar_dia(valor):
    return f"{_como_data(valor).day:02d}"


def formatar_mes_abreviado(valor):
    return MESES[_como_data(valor).month - 1][:3]


def formatar_dia_da_semana_abreviado(valor):
    return DIAS_DA_SEMANA[_como_data(valor).weekday()][:3]


def formatar_status(valor):
    return valor.capitalize()


def preparar_reserva_para_tela(reserva, hoje):
    futura = reserva["data_reserva"] >= hoje.isoformat()
    confirmada = reserva["status"] == "CONFIRMADA"
    if not confirmada:
        rotulo_status, classe_status = "Cancelada", "cancelada"
    elif futura:
        rotulo_status, classe_status = "Confirmada", "confirmada"
    else:
        rotulo_status, classe_status = "Concluída", "concluida"
    return {
        **reserva,
        "rotulo_status": rotulo_status,
        "classe_status": classe_status,
        "pode_cancelar": confirmada and futura,
    }


def separar_reservas(reservas, hoje):
    preparadas = [preparar_reserva_para_tela(reserva, hoje) for reserva in reservas]
    proximas = [r for r in preparadas if r["classe_status"] == "confirmada"]
    historico = [r for r in preparadas if r["classe_status"] != "confirmada"]
    proximas.sort(key=lambda r: (r["data_reserva"], r["hora_inicio"]))
    historico.sort(key=lambda r: (r["data_reserva"], r["hora_inicio"]), reverse=True)
    return proximas, historico
