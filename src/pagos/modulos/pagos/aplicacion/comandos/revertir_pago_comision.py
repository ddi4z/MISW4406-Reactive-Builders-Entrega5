from datetime import datetime
import logging
from pagos.modulos.pagos.dominio.eventos import PagoRevertido
from pagos.modulos.pagos.dominio.entidades import Pago
from pagos.modulos.pagos.dominio.repositorios import RepositorioEventosPagos, RepositorioPagos
from pagos.seedwork.aplicacion.comandos import Comando
from pagos.modulos.pagos.aplicacion.dto import PagoDTO
from .base import RevertirPagoComisionBaseHandler
from dataclasses import dataclass
from pagos.seedwork.aplicacion.comandos import ejecutar_commando as comando

from pagos.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from pagos.modulos.pagos.aplicacion.mapeadores import MapeadorPago

@dataclass
class RevertirPagoComision(Comando):
    id_pago: str
    id_correlacion: str
    fecha_creacion: str
    fecha_actualizacion: str
    motivo: str = ""

class RevertirPagoComisionHandler(RevertirPagoComisionBaseHandler):

    def handle(self, comando: RevertirPagoComision):
        evento = PagoRevertido(
            id_pago=comando.id_pago,
            id_correlacion=comando.id_correlacion,
            motivo=comando.motivo,
            fecha_cancelacion=datetime.now()
        )

        agregada = Pago()
        agregada.agregar_evento(evento)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPagos)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosPagos)

        UnidadTrabajoPuerto.registrar_batch(
            repositorio.revertir,
            comando.id_pago  
        )

 
        UnidadTrabajoPuerto.registrar_batch(
            lambda _: None,
            agregada,
            repositorio_eventos_func=repositorio_eventos.agregar,
        )

      
        UnidadTrabajoPuerto.commit()

        logging.info(
            f"[SAGA] PagoCancelado emitido (corr={comando.id_correlacion}, id={comando.id_pago})"
        )

@comando.register(RevertirPagoComision)
def ejecutar_comando_crear_pago(comando: RevertirPagoComision):
    handler = RevertirPagoComisionHandler()
    handler.handle(comando)
    