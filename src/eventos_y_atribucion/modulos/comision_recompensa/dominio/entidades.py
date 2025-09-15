"""Entidades del dominio de recompensas y comisiones

En este archivo usted encontrará las entidades del dominio de recompensas y comisiones

"""

from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field
import uuid



import eventos_y_atribucion.modulos.comision_recompensa.dominio.objetos_valor as ov
from eventos_y_atribucion.modulos.comision_recompensa.dominio.eventos import ComisionCreada, RecompensaCreada
from eventos_y_atribucion.seedwork.dominio.entidades import AgregacionRaiz

"""
    RECOMPENSA   
"""


@dataclass
class Recompensa(AgregacionRaiz):
    id_evento: uuid = field(default_factory=uuid)
    descripcion: str = field(default_factory=str)

    def crear_recompensa(self, recompensa: Recompensa):
        self.id_evento = recompensa.id_evento
        self.descripcion = recompensa.descripcion
        self.agregar_evento(RecompensaCreada(id_recompensa=self.id, fecha_creacion=self.fecha_creacion, id_evento=self.id_evento, descripcion=self.descripcion))




"""
    COMISIONES
"""
@dataclass
class Comision(AgregacionRaiz, ABC):
    id_evento: uuid.UUID = field(hash=True, default=None)
    monto_comision: ov.MontoComision = field(default_factory=ov.MontoComision)
    
    def crear_comision(self, comision: Comision):
        self.id_evento = comision.id_evento
        self.monto_comision = comision.monto_comision

        self.agregar_evento(ComisionCreada(id=self.id, id_evento=self.id_evento, valor=self.monto_comision.valor, fecha_creacion=self.fecha_creacion ))



