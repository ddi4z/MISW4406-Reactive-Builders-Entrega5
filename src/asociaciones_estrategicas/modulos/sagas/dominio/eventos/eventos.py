
from dataclasses import dataclass
from datetime import datetime
import uuid
from asociaciones_estrategicas.seedwork.dominio.eventos import EventoDominio

@dataclass
class EventoCreado(EventoDominio):
    id_evento: uuid.UUID | None = None
    id_asociacion: uuid.UUID | None = None
    id_correlacion: str | None = None
    fecha: datetime | None = None

@dataclass
class EventoFallido(EventoDominio):
    id_asociacion: uuid.UUID | None = None
    id_correlacion: str | None = None
    razon: str | None = None
    fecha: datetime | None = None

@dataclass
class EventoCancelado(EventoDominio):
    id_evento: uuid.UUID | None = None
    id_asociacion: uuid.UUID | None = None
    id_correlacion: str | None = None
    fecha: datetime | None = None
