from app.database import transacao
from app.models.reserva import Reserva
from app.repositories.espaco_repository import EspacoRepository
from app.repositories.reserva_repository import ReservaRepository
from app.services.opcoes_horario import gerar_opcoes
from app.utils.excecoes import (
    ConflitoHorarioErro,
    NaoEncontradoErro,
    PermissaoNegadaErro,
    ValidacaoErro,
)
from app.utils.tempo import formatar_hora
from app.utils.validadores import (
    validar_data,
    validar_data_nao_passada,
    validar_hora,
    validar_inteiro_positivo,
    validar_intervalo_horario,
)


class ReservaService:
    def __init__(self, repositorio_reservas=None, repositorio_espacos=None):
        self._reservas = repositorio_reservas or ReservaRepository()
        self._espacos = repositorio_espacos or EspacoRepository()

    def criar(self, usuario, dados):
        id_espaco = validar_inteiro_positivo(dados.get("id_espaco"), "id_espaco")
        data_reserva = validar_data(dados.get("data_reserva"), "data_reserva")
        hora_inicio = validar_hora(dados.get("hora_inicio"), "hora_inicio")
        hora_fim = validar_hora(dados.get("hora_fim"), "hora_fim")
        validar_intervalo_horario(hora_inicio, hora_fim)
        validar_data_nao_passada(data_reserva)

        with transacao() as conexao:
            espaco = self._espacos.buscar_por_id(id_espaco, conexao, bloquear=True)
            if espaco is None:
                raise NaoEncontradoErro("Espaço não encontrado")
            if not espaco.ativo:
                raise ValidacaoErro("Este espaço está desativado")
            if not espaco.comporta_horario(hora_inicio, hora_fim):
                raise ValidacaoErro("Horário fora do funcionamento do espaço")

            nova_reserva = Reserva(
                usuario.id_usuario, id_espaco, data_reserva, hora_inicio, hora_fim
            )
            reservas_existentes = self._reservas.listar_confirmadas_do_espaco_na_data(
                id_espaco, data_reserva, conexao
            )
            if not espaco.esta_disponivel(nova_reserva, reservas_existentes):
                raise ConflitoHorarioErro("Horário indisponível")

            nova_reserva.id_reserva = self._reservas.criar(nova_reserva, conexao)
            return self._reservas.buscar_por_id(nova_reserva.id_reserva, conexao)

    def listar_opcoes_de_horario(self, espaco, data_reserva):
        reservas_confirmadas = self._reservas.listar_confirmadas_do_espaco_na_data(
            espaco.id_espaco, data_reserva
        )
        return gerar_opcoes(espaco, reservas_confirmadas, data_reserva)

    def reservar_opcao(self, usuario, espaco, data_texto, id_opcao):
        data_reserva = validar_data(data_texto, "data")
        opcoes = gerar_opcoes(espaco, [], data_reserva)
        escolhida = next((o for o in opcoes if o.id_opcao == id_opcao), None)
        if escolhida is None:
            raise ValidacaoErro("Escolha um horário")
        return self.criar(
            usuario,
            {
                "id_espaco": espaco.id_espaco,
                "data_reserva": data_reserva.isoformat(),
                "hora_inicio": formatar_hora(escolhida.hora_inicio),
                "hora_fim": formatar_hora(escolhida.hora_fim),
            },
        )

    def buscar_propria(self, usuario, id_reserva):
        reserva = self._reservas.buscar_por_id(id_reserva)
        if reserva is None or reserva.id_usuario != usuario.id_usuario:
            raise NaoEncontradoErro("Reserva não encontrada")
        return reserva

    def listar_do_usuario(self, usuario):
        return self._reservas.listar_do_usuario(usuario.id_usuario)

    def listar_todas(self, usuario, id_espaco=None, data_reserva=None):
        if not usuario.pode_ver_todas_as_reservas():
            raise PermissaoNegadaErro("Apenas administradores veem todas as reservas")
        return self._reservas.listar_todas(id_espaco, data_reserva)

    def cancelar(self, usuario, id_reserva):
        reserva = self._reservas.buscar_por_id(id_reserva)
        if reserva is None:
            raise NaoEncontradoErro("Reserva não encontrada")
        if not usuario.pode_cancelar_reserva(reserva):
            raise PermissaoNegadaErro("Você só pode cancelar as suas próprias reservas")
        reserva.cancelar()
        self._reservas.atualizar_status(reserva)
        return reserva
