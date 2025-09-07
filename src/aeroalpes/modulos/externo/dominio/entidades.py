"""Entidades del dominio de externo

En este archivo usted encontrará las entidades del dominio de externo

"""

from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
import uuid



import aeroalpes.modulos.externo.dominio.objetos_valor as ov
from aeroalpes.modulos.externo.dominio.eventos import EventoCreado, MedioMarketingCreado, PlataformaCreada, PublicacionCreada
from aeroalpes.seedwork.dominio.entidades import AgregacionRaiz, Entidad

"""
    PUBLICACIONES   
"""

@dataclass
class Publicacion(Entidad):
    ...
    
@dataclass
class Plataforma(Entidad):
    ...

@dataclass
class MedioMarketing(AgregacionRaiz):
    tipo_publicacion: ov.TipoPublicacion = field(default_factory=ov.TipoPublicacion)
    plataforma: Plataforma = field(default_factory=Plataforma)
    
    def crear_medio_marketing(self, medio: MedioMarketing):
        self.tipo_publicacion = medio.tipo_publicacion
        self.agregar_evento(MedioMarketingCreado(id_medioMarketing=self.id, fecha_creacion=self.fecha_creacion, id_plataforma=self.plataforma.id))
        
    def crear_publicacion(self, publicacion: Publicacion):
        self.agregar_evento(PublicacionCreada(id_publicacion=publicacion.id, fecha_creacion=self.fecha_creacion, id_medioMarketing=self.id))
        
    def crear_plataforma(self, plataforma: Plataforma):
        self.agregar_evento(PlataformaCreada(id_plataforma=plataforma.id, fecha_creacion=self.fecha_creacion))
    ...




"""
    EVENTOS
"""
@dataclass
class Evento(AgregacionRaiz, ABC):
    id_publicacion: uuid.UUID = field(hash=True, default=None)
    fecha_evento: datetime = field(default_factory=datetime.now)
    
    def crear_evento(self, evento: Evento):
        self.id_publicacion = evento.id_publicacion
        self.fecha_evento = evento.fecha_evento

        self.agregar_evento(EventoCreado(id_evento=self.id, id_publicacion=self.id_publicacion, tipo_evento=self.__class__.__name__, fecha_creacion=self.fecha_evento))

class Lead(Evento):
    ...
    
    
class InteraccionPublicacion(Evento):
    ...
