"""Entidades del dominio de recompensas y comisiones

En este archivo usted encontrará las entidades del dominio de recompensas y comisiones

"""

from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
import uuid

from pagos.seedwork.dominio.entidades import AgregacionRaiz
from pagos.modulos.pagos.dominio.eventos import PagoRealizado


@dataclass
class Pago(AgregacionRaiz):
    id_comision: uuid.UUID = field(default_factory=uuid.uuid4)
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_actualizacion: datetime = field(default_factory=datetime.now)
    id_correlacion: str = field(default_factory=str)
    moneda: str = field(default_factory=str)
    monto: float = field(default_factory=float)
    metodo_pago: str = field(default_factory=str)
    estado: str = field(default_factory=str)
    pasarela: str = field(default_factory=str)

    def crear_pago(self, pago: Pago):
        self.fecha_creacion = pago.fecha_creacion
        self.id_comision = pago.id_comision
        self.fecha_actualizacion = self.fecha_creacion
        self.id_correlacion = pago.id_correlacion
        self.moneda = pago.moneda
        self.monto = pago.monto
        self.metodo_pago = pago.metodo_pago
        self.estado = pago.estado
        self.pasarela = pago.pasarela
 
        self.agregar_evento(PagoRealizado( 
            id_comision = self.id_comision,
            fecha_actualizacion =  self.fecha_actualizacion,
            fecha_creacion = self.fecha_creacion,
            id_correlacion =  self.id_correlacion,
            moneda = self.moneda,
            monto = self.monto,
            metodo_pago = self.metodo_pago,
            estado = self.estado,
            pasarela = self.pasarela
            ))
        
 



