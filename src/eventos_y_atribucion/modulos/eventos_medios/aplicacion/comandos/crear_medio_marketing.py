from eventos_y_atribucion.modulos.eventos_medios.aplicacion.mapeadores import MapeadorMedioMarketing
from eventos_y_atribucion.modulos.eventos_medios.dominio.entidades import MedioMarketing
from eventos_y_atribucion.modulos.eventos_medios.dominio.repositorios import RepositorioMediosMarketing
from eventos_y_atribucion.seedwork.aplicacion.comandos import Comando
from eventos_y_atribucion.modulos.eventos_medios.aplicacion.dto import MedioMarketingDTO
from .base import CrearMedioMarketingBaseHandler
from dataclasses import dataclass
from eventos_y_atribucion.seedwork.aplicacion.comandos import ejecutar_commando as comando

from eventos_y_atribucion.seedwork.infraestructura.uow import UnidadTrabajoPuerto



@dataclass
class CrearMedioMarketing(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str



class CrearMedioMarketingHandler(CrearMedioMarketingBaseHandler):

    def handle(self, comando: CrearMedioMarketing):
        medio_dto = MedioMarketingDTO(
            fecha_actualizacion=comando.fecha_actualizacion,
            fecha_creacion=comando.fecha_creacion,
            id=comando.id
        )

        medio: MedioMarketing = self.fabrica_medios_marketing.crear_objeto(medio_dto, MapeadorMedioMarketing())
        medio.crear_medio_marketing(medio)
        

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioMediosMarketing)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, medio)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearMedioMarketing)
def ejecutar_comando_crear_medio_marketing(comando: CrearMedioMarketing):
    handler = CrearMedioMarketingHandler()
    handler.handle(comando)
    