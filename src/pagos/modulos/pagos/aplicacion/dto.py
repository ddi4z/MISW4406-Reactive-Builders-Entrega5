from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
import uuid
from pagos.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class PagoDTO(DTO):
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    id_comision: str = field(default_factory=lambda: str(uuid.uuid4()))
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_actualizacion: datetime = field(default_factory=datetime.now)
    id_correlacion: str = field(default_factory=str)
    moneda: str = field(default_factory=str)
    monto: float = field(default_factory=float)
    metodo_pago: str = field(default_factory=str)
    estado: str = field(default_factory=str)
    pasarela: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
