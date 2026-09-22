"""
Regras de negócio de reserva — o coração do sistema.

Inclui `esta_disponivel()`, citado literalmente no comentário do
script SQL do banco como a regra "validada na camada de aplicação,
no método esta_disponivel() da classe Espaco". Aqui ela vive no
service (mantendo o model Espaco mais simples), mas o nome e o
comportamento são exatamente os combinados na modelagem.
"""

from __future__ import annotations

from datetime import date, time

from app.models.espaco import Espaco
from app.models.reserva import Reserva, StatusReserva
from app.models.usuario import Usuario
from app.repositories.espaco_repository import EspacoRepository
from app.repositories.reserva_repository import ReservaRepository
from app.services.espaco_service import PermissaoNegadaError
from app.utils.validators import validar_horario


class ConflitoDeHorarioError(Exception):
    """Levantada quando o horário pedido colide com uma reserva já confirmada."""


class ReservaService:
    """Casos de uso: criar, listar e cancelar reservas."""

    def __init__(
        self,
        reserva_repository: ReservaRepository | None = None,
        espaco_repository: EspacoRepository | None = None,
    ):
        self.reserva_repository = reserva_repository or ReservaRepository()
        self.espaco_repository = espaco_repository or EspacoRepository()

    def esta_disponivel(self, espaco: Espaco, data_reserva: date, hora_inicio: time, hora_fim: time) -> bool:
        """
        Busca as reservas já CONFIRMADAs do mesmo espaço/data e
        verifica se alguma delas se sobrepõe ao horário pedido
        (Reserva.sobrepoe cuida da comparação de intervalos).
        """
        candidata = Reserva(
            id_reserva=None,
            id_usuario=0,
            id_espaco=espaco.id_espaco,
            data_reserva=data_reserva,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
        )
        existentes = self.reserva_repository.listar_por_espaco_e_data(espaco.id_espaco, data_reserva)
        return not any(candidata.sobrepoe(existente) for existente in existentes)

    def criar_reserva(
        self,
        morador: Usuario,
        id_espaco: int,
        data_reserva: date,
        hora_inicio: time,
        hora_fim: time,
    ) -> Reserva:
        """Fluxo 'Fazer reserva' do fluxograma, com todas as validações do caminho."""
        validar_horario(hora_inicio, hora_fim)

        espaco = self.espaco_repository.buscar_por_id(id_espaco)
        if espaco is None or not espaco.ativo:
            raise ValueError("Espaço não encontrado ou inativo.")
        if not espaco.dentro_do_horario_de_funcionamento(hora_inicio, hora_fim):
            raise ValueError("Horário fora do funcionamento do espaço.")
        if not self.esta_disponivel(espaco, data_reserva, hora_inicio, hora_fim):
            raise ConflitoDeHorarioError("Horário indisponível para este espaço.")

        return self.reserva_repository.criar(morador.id_usuario, id_espaco, data_reserva, hora_inicio, hora_fim)

    def listar_minhas_reservas(self, usuario: Usuario) -> list[Reserva]:
        return self.reserva_repository.listar_por_usuario(usuario.id_usuario)

    def listar_todas(self, solicitante: Usuario) -> list[Reserva]:
        if not solicitante.pode_gerenciar_qualquer_reserva():
            raise PermissaoNegadaError("Apenas administradores podem ver todas as reservas.")
        return self.reserva_repository.listar_todas()

    def cancelar(self, solicitante: Usuario, id_reserva: int) -> None:
        """Um morador só cancela a própria reserva; o admin cancela qualquer uma."""
        reserva = self.reserva_repository.buscar_por_id(id_reserva)
        if reserva is None:
            raise ValueError("Reserva não encontrada.")

        eh_dono = reserva.id_usuario == solicitante.id_usuario
        eh_admin = solicitante.pode_gerenciar_qualquer_reserva()
        if not (eh_dono or eh_admin):
            raise PermissaoNegadaError("Você não tem permissão para cancelar esta reserva.")

        self.reserva_repository.cancelar(id_reserva)
