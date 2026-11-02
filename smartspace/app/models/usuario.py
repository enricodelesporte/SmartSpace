from abc import ABC, abstractmethod

from app.utils.excecoes import ValidacaoErro


class Usuario(ABC):
    TIPO = None

    def __init__(self, nome, email, senha_hash, id_usuario=None, data_cadastro=None, ativo=True):
        self._id_usuario = id_usuario
        self._nome = nome
        self._email = email
        self._senha_hash = senha_hash
        self._data_cadastro = data_cadastro
        self._ativo = ativo

    @property
    def id_usuario(self):
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, valor):
        self._id_usuario = valor

    @property
    def nome(self):
        return self._nome

    @property
    def email(self):
        return self._email

    @property
    def senha_hash(self):
        return self._senha_hash

    @property
    def data_cadastro(self):
        return self._data_cadastro

    @property
    def ativo(self):
        return self._ativo

    @property
    def tipo_usuario(self):
        return self.TIPO

    def alterar_nome(self, novo_nome):
        self._nome = novo_nome

    def alterar_senha_hash(self, novo_hash):
        self._senha_hash = novo_hash

    @abstractmethod
    def pode_gerenciar_espacos(self):
        ...

    @abstractmethod
    def pode_ver_todas_as_reservas(self):
        ...

    @abstractmethod
    def pode_cancelar_reserva(self, reserva):
        ...

    def para_dicionario(self):
        return {
            "id_usuario": self._id_usuario,
            "nome": self._nome,
            "email": self._email,
            "tipo_usuario": self.tipo_usuario,
            "ativo": self._ativo,
            "data_cadastro": self._data_cadastro.isoformat()
            if self._data_cadastro
            else None,
        }


class Admin(Usuario):
    TIPO = "ADMIN"

    def pode_gerenciar_espacos(self):
        return True

    def pode_ver_todas_as_reservas(self):
        return True

    def pode_cancelar_reserva(self, reserva):
        return True


class Morador(Usuario):
    TIPO = "MORADOR"

    def pode_gerenciar_espacos(self):
        return False

    def pode_ver_todas_as_reservas(self):
        return False

    def pode_cancelar_reserva(self, reserva):
        return reserva.id_usuario == self.id_usuario


class UsuarioFactory:
    CLASSES_POR_TIPO = {Admin.TIPO: Admin, Morador.TIPO: Morador}

    @classmethod
    def criar(cls, tipo_usuario, nome, email, senha_hash, **campos_opcionais):
        classe = cls.CLASSES_POR_TIPO.get(tipo_usuario)
        if classe is None:
            raise ValidacaoErro("Tipo de usuário inválido")
        return classe(nome, email, senha_hash, **campos_opcionais)

    @classmethod
    def a_partir_do_registro(cls, registro):
        return cls.criar(
            registro["tipo_usuario"],
            registro["nome"],
            registro["email"],
            registro["senha_hash"],
            id_usuario=registro["id_usuario"],
            data_cadastro=registro["data_cadastro"],
            ativo=bool(registro["ativo"]),
        )
