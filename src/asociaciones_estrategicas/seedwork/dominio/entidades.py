"""Entidades reusables parte del seedwork del proyecto

En este archivo usted encontrará las entidades reusables parte del seedwork del proyecto

"""

from dataclasses import dataclass, field
from .eventos import EventoDominio
from .mixins import ValidarReglasMixin
from .reglas import IdEntidadEsInmutable
from .excepciones import IdDebeSerInmutableExcepcion
from datetime import datetime
import uuid

@dataclass
class Entidad:
    _id: uuid.UUID = field(default=None, init=False, repr=False)
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_actualizacion: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        # Si no hay id asignado, se genera automáticamente
        if self._id is None:
            self._id = self.siguiente_id()

    @classmethod
    def siguiente_id(cls) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @id.setter
    def id(self, value: uuid.UUID) -> None:
        # solo permite asignar una vez (para reconstrucción desde BD)
        if getattr(self, "_id", None) is not None:
            raise IdDebeSerInmutableExcepcion()
        self._id = value if value else self.siguiente_id()
        

@dataclass
class AgregacionRaiz(Entidad, ValidarReglasMixin):
    eventos: list[EventoDominio] = field(default_factory=list)
    eventos_compensacion: list[EventoDominio] = field(default_factory=list)

    def agregar_evento(self, evento: EventoDominio, evento_compensacion: EventoDominio = None):
        self.eventos.append(evento)

        if evento_compensacion:
            self.eventos_compensacion.append(evento_compensacion)
    
    def limpiar_eventos(self):
        self.eventos = list()
        self.eventos_compensacion = list()


@dataclass
class Locacion(Entidad):
    def __str__(self) -> str:
        ...