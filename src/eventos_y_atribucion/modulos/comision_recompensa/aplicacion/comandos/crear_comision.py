from eventos_y_atribucion.modulos.comision_recompensa.dominio.entidades import Comision
from eventos_y_atribucion.modulos.comision_recompensa.dominio.repositorios import RepositorioComisiones
from eventos_y_atribucion.seedwork.aplicacion.comandos import Comando
from eventos_y_atribucion.modulos.comision_recompensa.aplicacion.dto import ComisionDTO
from .base import CrearComisionBaseHandler
from dataclasses import dataclass
from eventos_y_atribucion.seedwork.aplicacion.comandos import ejecutar_commando as comando

from eventos_y_atribucion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from eventos_y_atribucion.modulos.comision_recompensa.aplicacion.mapeadores import MapeadorComision


@dataclass
class CrearComision(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    id_evento: str
    valor: int = 2


class CrearComisionHandler(CrearComisionBaseHandler):

      def handle(self, comando: CrearComision):

        comision_dto = ComisionDTO(
            fecha_actualizacion=comando.fecha_actualizacion,
            fecha_creacion=comando.fecha_creacion,
            id=comando.id,
            id_evento=comando.id_evento,
            valor=comando.valor
        )

        comision: Comision = self.fabrica_comisiones.crear_objeto(comision_dto, MapeadorComision())
        comision.crear_comision(comision)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioComisiones)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, comision)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearComision)
def ejecutar_comando_crear_publicacion(comando: CrearComision):
    handler = CrearComisionHandler()
    handler.handle(comando)
    