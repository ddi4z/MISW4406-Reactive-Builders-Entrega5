from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
import uuid
from alpespartners.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

@dataclass
class RecompensaCreada(EventoDominio):
    id_recompensa: uuid.UUID = None
    descripcion: str = None
    id_evento: uuid.UUID = None
    fecha_creacion: datetime = None

@dataclass
class ComisionCreada(EventoDominio):
    id_comision: uuid.UUID = None
    valor: int = None
    id_evento: uuid.UUID = None
    fecha_creacion: datetime = None