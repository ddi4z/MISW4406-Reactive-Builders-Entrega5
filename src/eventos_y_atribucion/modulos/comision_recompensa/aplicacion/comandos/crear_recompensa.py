from abc import ABC
from eventos_y_atribucion.modulos.comision_recompensa.dominio.entidades import Recompensa
from eventos_y_atribucion.modulos.comision_recompensa.aplicacion.dto import RecompensaDTO
from eventos_y_atribucion.modulos.comision_recompensa.dominio.repositorios import RepositorioRecompensas
from eventos_y_atribucion.seedwork.aplicacion.comandos import Comando
from .base import CrearRecompensaBaseHandler
from dataclasses import dataclass
from eventos_y_atribucion.seedwork.aplicacion.comandos import ejecutar_commando as comando

from eventos_y_atribucion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from eventos_y_atribucion.modulos.comision_recompensa.aplicacion.mapeadores import MapeadorRecompensa


@dataclass
class CrearRecompensa(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    id_evento:str
    descripcion:str = ""


class CrearRecompensaHandler(CrearRecompensaBaseHandler):

    def handle(self, comando: CrearRecompensa):
        recompensa_dto = RecompensaDTO(
            id=comando.id,
            descripcion = comando.descripcion,
            fecha_actualizacion=comando.fecha_actualizacion,
            fecha_creacion=comando.fecha_creacion,
            id_evento=comando.id_evento,
        )

        recompensa: Recompensa = self.fabrica_recompensas.crear_objeto(recompensa_dto, MapeadorRecompensa())
        recompensa.crear_recompensa(recompensa)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioRecompensas)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, recompensa)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearRecompensa)
def ejecutar_comando_crear_recompensa(comando: CrearRecompensa):
    handler = CrearRecompensaHandler()
    handler.handle(comando)
    