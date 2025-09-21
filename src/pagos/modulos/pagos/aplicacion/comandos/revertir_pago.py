from pagos.modulos.pagos.dominio.entidades import Pago
from pagos.modulos.pagos.dominio.repositorios import RepositorioPagos
from pagos.seedwork.aplicacion.comandos import Comando
from pagos.modulos.pagos.aplicacion.dto import PagoDTO
from .base import RevertirPagoComisionBaseHandler
from dataclasses import dataclass
from pagos.seedwork.aplicacion.comandos import ejecutar_commando as comando

from pagos.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from pagos.modulos.pagos.aplicacion.mapeadores import MapeadorPago

@dataclass
class RevertirPagoComision(Comando):
    id: str

class RevertirPagoComisionHandler(RevertirPagoComisionBaseHandler):

      def handle(self, comando: RevertirPagoComision):
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPagos)
        
        UnidadTrabajoPuerto.registrar_batch(repositorio.revertir, comando.id)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@comando.register(RevertirPagoComision)
def ejecutar_comando_crear_pago(comando: RevertirPagoComision):
    handler = RevertirPagoComisionHandler()
    handler.handle(comando)
    