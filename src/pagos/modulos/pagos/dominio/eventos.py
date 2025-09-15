from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
import uuid
from pagos.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

@dataclass
class PagoCreado(EventoDominio):
    id_comision: uuid.UUID = None
    fecha_actualizacion: datetime = None
    fecha_creacion: datetime = None
    id_correlacion: str = None
    moneda: str = None
    monto: float = None
    metodo_pago: str = None
    estado: str = None
    pasarela: str = None