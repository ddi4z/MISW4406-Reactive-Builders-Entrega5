from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field
import uuid
from eventos_y_atribucion.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime


@dataclass
class EventoCreado(EventoDominio):
    id_correlacion: str = None
    id_evento: uuid.UUID = None
    tipo_evento: str = None
    id_publicacion: uuid.UUID = None
    fecha_creacion: datetime = None
    fecha_actualizacion: datetime = field(default_factory=datetime.now)
    
@dataclass
class EventoFallido(EventoDominio):
    id_correlacion: str = None
    id_evento: uuid.UUID = None
    tipo_evento: str = None
    id_publicacion: uuid.UUID = None
    fecha_creacion: datetime = None
    fecha_actualizacion: datetime = field(default_factory=datetime.now)
    
@dataclass
class EventoCancelado(EventoDominio):
    id_correlacion: str = None
    id_evento: uuid.UUID = None
    tipo_evento: str = None
    id_publicacion: uuid.UUID = None
    fecha_creacion: datetime = None
    fecha_actualizacion: datetime = field(default_factory=datetime.now)
   
@dataclass
class MedioMarketingCreado(EventoDominio):
    id_medioMarketing: uuid.UUID = None
    fecha_creacion: datetime = None
    nombre_plataforma: str = None
    
@dataclass
class PublicacionCreada(EventoDominio):
    id_publicacion: uuid.UUID = None
    fecha_creacion: datetime = None
    id_medioMarketing: uuid.UUID = None
    
@dataclass
class PlataformaCreada(EventoDominio):
    id_plataforma: uuid.UUID = None
    fecha_creacion: datetime = None