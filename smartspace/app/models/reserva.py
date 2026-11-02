from app.utils.excecoes import ValidacaoErro
from app.utils.tempo import formatar_hora, para_time


class Reserva:
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"

    def __init__(
        self,
        id_usuario,
        id_espaco,
        data_reserva,
        hora_inicio,
        hora_fim,
        status=CONFIRMADA,
        id_reserva=None,
        data_criacao=None,
        nome_espaco=None,
        nome_usuario=None,
    ):
        self._id_reserva = id_reserva
        self._id_usuario = id_usuario
        self._id_espaco = id_espaco
        self._data_reserva = data_reserva
        self._hora_inicio = hora_inicio
        self._hora_fim = hora_fim
        self._status = status
        self._data_criacao = data_criacao
        self.nome_espaco = nome_espaco
        self.nome_usuario = nome_usuario

    @property
    def id_reserva(self):
        return self._id_reserva

    @id_reserva.setter
    def id_reserva(self, valor):
        self._id_reserva = valor

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def id_espaco(self):
        return self._id_espaco

    @property
    def data_reserva(self):
        return self._data_reserva

    @property
    def hora_inicio(self):
        return self._hora_inicio

    @property
    def hora_fim(self):
        return self._hora_fim

    @property
    def status(self):
        return self._status

    @property
    def esta_cancelada(self):
        return self._status == self.CANCELADA

    def cancelar(self):
        if self.esta_cancelada:
            raise ValidacaoErro("Esta reserva já está cancelada")
        self._status = self.CANCELADA

    def sobrepoe_horario_de(self, outra):
        return self._hora_inicio < outra.hora_fim and outra.hora_inicio < self._hora_fim

    def conflita_com(self, outra):
        if self.esta_cancelada or outra.esta_cancelada:
            return False
        if self._id_espaco != outra.id_espaco or self._data_reserva != outra.data_reserva:
            return False
        return self.sobrepoe_horario_de(outra)

    @classmethod
    def a_partir_do_registro(cls, registro):
        return cls(
            id_usuario=registro["id_usuario"],
            id_espaco=registro["id_espaco"],
            data_reserva=registro["data_reserva"],
            hora_inicio=para_time(registro["hora_inicio"]),
            hora_fim=para_time(registro["hora_fim"]),
            status=registro["status"],
            id_reserva=registro["id_reserva"],
            data_criacao=registro["data_criacao"],
            nome_espaco=registro.get("nome_espaco"),
            nome_usuario=registro.get("nome_usuario"),
        )

    def para_dicionario(self):
        return {
            "id_reserva": self._id_reserva,
            "id_usuario": self._id_usuario,
            "id_espaco": self._id_espaco,
            "nome_espaco": self.nome_espaco,
            "nome_usuario": self.nome_usuario,
            "data_reserva": self._data_reserva.isoformat(),
            "hora_inicio": formatar_hora(self._hora_inicio),
            "hora_fim": formatar_hora(self._hora_fim),
            "status": self._status,
            "data_criacao": self._data_criacao.isoformat()
            if self._data_criacao
            else None,
        }
