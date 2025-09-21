from pagos.modulos.pagos.dominio.entidades import Pago
from pagos.modulos.pagos.dominio.repositorios import RepositorioPagos
from pagos.seedwork.aplicacion.comandos import Comando
from pagos.modulos.pagos.aplicacion.dto import PagoDTO
from .base import RealizarPagoComisionBaseHandler
from dataclasses import dataclass
from pagos.seedwork.aplicacion.comandos import ejecutar_commando as comando

from pagos.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from pagos.modulos.pagos.aplicacion.mapeadores import MapeadorPago

@dataclass
class RealizarPagoComision(Comando):
    id: str
    fecha_creacion: str
    fecha_actualizacion: str
    id_correlacion: str
    id_comision: str
    moneda: str
    monto: float
    metodo_pago: str
    estado: str
    pasarela: str

class RealizarPagoComisionHandler(RealizarPagoComisionBaseHandler):

      def handle(self, comando: RealizarPagoComision):

        pago_dto = PagoDTO(
            fecha_actualizacion = comando.fecha_actualizacion,
            fecha_creacion = comando.fecha_creacion,
            id = comando.id,
            id_correlacion = comando.id_correlacion,
            id_comision = comando.id_comision,
            moneda = comando.moneda,
            monto = comando.monto,
            metodo_pago = comando.metodo_pago,
            estado = comando.estado,
            pasarela = comando.pasarela
        )
        print("*" * 100)
        
        pago: Pago = self.fabrica_pagos.crear_objeto(pago_dto, MapeadorPago())
        pago.crear_pago(pago)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPagos)

        print(pago)
        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, pago)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(RealizarPagoComision)
def ejecutar_comando_crear_pago(comando: RealizarPagoComision):
    handler = RealizarPagoComisionHandler()
    handler.handle(comando)
    