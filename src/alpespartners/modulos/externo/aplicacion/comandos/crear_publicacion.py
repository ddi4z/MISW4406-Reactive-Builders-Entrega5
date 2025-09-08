from alpespartners.modulos.externo.dominio.entidades import Publicacion
from alpespartners.modulos.externo.dominio.repositorios import RepositorioPublicaciones
from alpespartners.seedwork.aplicacion.comandos import Comando
from alpespartners.modulos.externo.aplicacion.dto import PublicacionDTO
from .base import CrearPublicacionBaseHandler
from dataclasses import dataclass
from alpespartners.seedwork.aplicacion.comandos import ejecutar_commando as comando

from alpespartners.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from alpespartners.modulos.externo.aplicacion.mapeadores import MapeadorPublicacion


@dataclass
class CrearPublicacion(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str



class CrearPublicacionHandler(CrearPublicacionBaseHandler):

    def handle(self, comando: CrearPublicacion):
        publicacion_dto = PublicacionDTO(
            fecha_actualizacion=comando.fecha_actualizacion,
            fecha_creacion=comando.fecha_creacion,
            id=comando.id,
        )

        publicacion: Publicacion = self.fabrica_publicaciones.crear_objeto(publicacion_dto, MapeadorPublicacion())
        publicacion.crear_publicacion(publicacion)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPublicaciones.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, publicacion)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearPublicacion)
def ejecutar_comando_crear_publicacion(comando: CrearPublicacion):
    handler = CrearPublicacionHandler()
    handler.handle(comando)
    