from pagos.modulos.pagos.dominio.entidades import Pago
from pagos.modulos.pagos.dominio.repositorios import RepositorioPagos
from pagos.seedwork.aplicacion.comandos import Comando
from pagos.modulos.pagos.aplicacion.dto import PagoDTO
from .base import RevertirPagoBaseHandler
from dataclasses import dataclass
from pagos.seedwork.aplicacion.comandos import ejecutar_commando as comando

from pagos.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from pagos.modulos.pagos.aplicacion.mapeadores import MapeadorPago

@dataclass
class RevertirPago(Comando):
    id: str

class RevertirPagoHandler(RevertirPagoBaseHandler):

      def handle(self, comando: RevertirPago):
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPagos)
        
        UnidadTrabajoPuerto.registrar_batch(repositorio.eliminar, comando.id)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@comando.register(RevertirPago)
def ejecutar_comando_crear_pago(comando: RevertirPago):
    handler = RevertirPagoHandler()
    handler.handle(comando)
    