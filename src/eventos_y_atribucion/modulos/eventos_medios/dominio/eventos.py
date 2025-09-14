from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
import uuid
from eventos_y_atribucion.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime


@dataclass
class EventoCreado(EventoDominio):
    id_evento: uuid.UUID = None
    tipo_evento: str = None
    id_publicacion: uuid.UUID = None
    fecha_creacion: datetime = None
   
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