from app.utils.tempo import formatar_hora, para_time


class Espaco:
    def __init__(
        self,
        nome,
        descricao,
        capacidade_maxima,
        horario_abertura,
        horario_fechamento,
        ativo=True,
        id_espaco=None,
    ):
        self._id_espaco = id_espaco
        self._nome = nome
        self._descricao = descricao
        self._capacidade_maxima = capacidade_maxima
        self._horario_abertura = horario_abertura
        self._horario_fechamento = horario_fechamento
        self._ativo = ativo

    @property
    def id_espaco(self):
        return self._id_espaco

    @id_espaco.setter
    def id_espaco(self, valor):
        self._id_espaco = valor

    @property
    def nome(self):
        return self._nome

    @property
    def descricao(self):
        return self._descricao

    @property
    def capacidade_maxima(self):
        return self._capacidade_maxima

    @property
    def horario_abertura(self):
        return self._horario_abertura

    @property
    def horario_fechamento(self):
        return self._horario_fechamento

    @property
    def ativo(self):
        return self._ativo

    def atualizar_dados(self, nome, descricao, capacidade_maxima, horario_abertura, horario_fechamento):
        self._nome = nome
        self._descricao = descricao
        self._capacidade_maxima = capacidade_maxima
        self._horario_abertura = horario_abertura
        self._horario_fechamento = horario_fechamento

    def desativar(self):
        self._ativo = False

    def comporta_horario(self, hora_inicio, hora_fim):
        return self._horario_abertura <= hora_inicio and hora_fim <= self._horario_fechamento

    def esta_disponivel(self, nova_reserva, reservas_existentes):
        return not any(
            existente.conflita_com(nova_reserva) for existente in reservas_existentes
        )

    @classmethod
    def a_partir_do_registro(cls, registro):
        return cls(
            nome=registro["nome"],
            descricao=registro["descricao"],
            capacidade_maxima=registro["capacidade_maxima"],
            horario_abertura=para_time(registro["horario_abertura"]),
            horario_fechamento=para_time(registro["horario_fechamento"]),
            ativo=bool(registro["ativo"]),
            id_espaco=registro["id_espaco"],
        )

    def para_dicionario(self):
        return {
            "id_espaco": self._id_espaco,
            "nome": self._nome,
            "descricao": self._descricao,
            "capacidade_maxima": self._capacidade_maxima,
            "horario_abertura": formatar_hora(self._horario_abertura),
            "horario_fechamento": formatar_hora(self._horario_fechamento),
            "ativo": self._ativo,
        }
