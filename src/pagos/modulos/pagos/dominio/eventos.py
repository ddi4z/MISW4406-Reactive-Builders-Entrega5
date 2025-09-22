from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field
import uuid
from pagos.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

@dataclass
class PagoRealizado(EventoDominio):
    id_pago: uuid.UUID = None
    id_comision: uuid.UUID = None
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_actualizacion: datetime = field(default_factory=datetime.now)
    id_correlacion: str = None
    moneda: str = None
    monto: float = None
    metodo_pago: str = None
    estado: str = None
    pasarela: str = None
    

@dataclass
class PagoFallido(EventoDominio):
    id_pago: uuid.UUID = None
    id_comision: uuid.UUID = None
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_actualizacion: datetime = field(default_factory=datetime.now)
    id_correlacion: str = None
    moneda: str = None
    monto: float = None
    metodo_pago: str = None
    estado: str = None
    pasarela: str = None
    motivo: str = ''
    
@dataclass
class PagoRevertido(EventoDominio):
    id_pago: uuid.UUID = None
    id_comision: uuid.UUID = None
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_actualizacion: datetime = field(default_factory=datetime.now)
    fecha_cancelacion: datetime = field(default_factory=datetime.now)
    id_correlacion: str = None
    moneda: str = None
    monto: float = None
    metodo_pago: str = None
    estado: str = None
    pasarela: str = None
    motivo: str = ''