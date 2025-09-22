
from dataclasses import dataclass
from datetime import datetime
import uuid
from asociaciones_estrategicas.seedwork.dominio.eventos import EventoDominio

@dataclass
class PagoRealizado(EventoDominio):
    id_pago: uuid.UUID | None = None
    id_asociacion: uuid.UUID | None = None
    id_correlacion: str | None = None
    monto: float | None = None
    monto_vat: float | None = None
    fecha: datetime | None = None

@dataclass
class PagoFallido(EventoDominio):
    id_asociacion: uuid.UUID | None = None
    id_correlacion: str | None = None
    razon: str | None = None
    fecha: datetime | None = None

@dataclass
class PagoRevertido(EventoDominio):
    id_pago: uuid.UUID | None = None
    id_asociacion: uuid.UUID | None = None
    id_correlacion: str | None = None
    fecha: datetime | None = None
