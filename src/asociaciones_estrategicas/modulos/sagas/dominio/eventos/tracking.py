
from dataclasses import dataclass
from datetime import datetime
import uuid
from asociaciones_estrategicas.seedwork.dominio.eventos import EventoDominio

@dataclass
class TrackingIniciado(EventoDominio):
    id_asociacion: uuid.UUID | None = None
    id_correlacion: str | None = None
    fecha: datetime | None = None

@dataclass
class InicioTrackingFallido(EventoDominio):
    id_asociacion: uuid.UUID | None = None
    id_correlacion: str | None = None
    razon: str | None = None
    fecha: datetime | None = None

@dataclass
class TrackingCancelado(EventoDominio):
    id_asociacion: uuid.UUID | None = None
    id_correlacion: str | None = None
    fecha: datetime | None = None
