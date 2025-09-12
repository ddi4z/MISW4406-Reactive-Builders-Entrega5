from __future__ import annotations
from dataclasses import dataclass, field
from asociaciones_estrategicas.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime
import uuid

class EventoAsociacionEstrategica(EventoDominio):
    ...

@dataclass
class AsociacionCreada(EventoAsociacionEstrategica):
    id_asociacion: uuid.UUID = None
    id_marca: uuid.UUID = None
    id_socio: uuid.UUID = None
    tipo: str = None
    fecha_creacion: datetime = None
    
@dataclass
class AsociacionFinalizada(EventoAsociacionEstrategica):
    id_asociacion: uuid.UUID = None
    fecha_actualizacion: datetime = None
