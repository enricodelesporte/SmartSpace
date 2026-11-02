from dataclasses import dataclass
from datetime import time

from app.models.reserva import Reserva
from app.utils.apresentacao import normalizar_texto
from app.utils.tempo import formatar_hora

HORARIOS_CHURRASQUEIRA = (
    ("manha", time(8, 0), time(15, 0)),
    ("noite", time(16, 0), time(22, 0)),
    ("dia", time(8, 0), time(22, 0)),
)
HORARIOS_SALAO = (("dia", time(8, 0), time(22, 0)),)
DESCRICOES_DAS_OPCOES = {
    "manha": "Manhã e almoço",
    "noite": "Final de tarde e noite",
    "dia": "Dia inteiro",
}


@dataclass(frozen=True)
class OpcaoHorario:
    id_opcao: str
    hora_inicio: time
    hora_fim: time
    disponivel: bool

    @property
    def descricao(self):
        return DESCRICOES_DAS_OPCOES.get(self.id_opcao, "")

    @property
    def rotulo(self):
        return f"{formatar_hora(self.hora_inicio)} – {formatar_hora(self.hora_fim)}"


def _horarios_base_do_espaco(espaco):
    nome = normalizar_texto(espaco.nome)
    if "churrasq" in nome:
        base = HORARIOS_CHURRASQUEIRA
    elif "salao" in nome or "festa" in nome:
        base = HORARIOS_SALAO
    else:
        base = ()
    cabem_no_funcionamento = [
        horario for horario in base if espaco.comporta_horario(horario[1], horario[2])
    ]
    if cabem_no_funcionamento:
        return cabem_no_funcionamento
    return [("dia", espaco.horario_abertura, espaco.horario_fechamento)]


def gerar_opcoes(espaco, reservas_confirmadas, data_reserva):
    opcoes = []
    for id_opcao, inicio, fim in _horarios_base_do_espaco(espaco):
        candidata = Reserva(0, espaco.id_espaco, data_reserva, inicio, fim)
        livre = espaco.esta_disponivel(candidata, reservas_confirmadas)
        opcoes.append(OpcaoHorario(id_opcao, inicio, fim, livre))
    return opcoes
