from aeroalpes.modulos.externo.aplicacion.mapeadores import MapeadorMedioMarketing
from aeroalpes.modulos.externo.dominio.entidades import MedioMarketing
from aeroalpes.modulos.externo.dominio.repositorios import RepositorioMediosMarketing
from aeroalpes.seedwork.aplicacion.comandos import Comando
from aeroalpes.modulos.externo.aplicacion.dto import MedioMarketingDTO
from .base import CrearPublicacionBaseHandler
from dataclasses import dataclass
from aeroalpes.seedwork.aplicacion.comandos import ejecutar_commando as comando

from aeroalpes.seedwork.infraestructura.uow import UnidadTrabajoPuerto



@dataclass
class CrearMedioMarketing(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str



class CrearMedioMarketingHandler(CrearPublicacionBaseHandler):

    def handle(self, comando: CrearMedioMarketing):
        medio_dto = MedioMarketingDTO(
            fecha_actualizacion=comando.fecha_actualizacion,
            fecha_creacion=comando.fecha_creacion,
            id=comando.id
        )

        medio: MedioMarketing = self.fabrica_publicaciones.crear_objeto(medio_dto, MapeadorMedioMarketing())
        medio.crear_medio(medio)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioMediosMarketing.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, medio)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearMedioMarketing)
def ejecutar_comando_crear_medio_marketing(comando: CrearMedioMarketing):
    handler = CrearMedioMarketingHandler()
    handler.handle(comando)
    