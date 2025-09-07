from alpespartners.modulos.externo.dominio.entidades import Plataforma, Publicacion
from alpespartners.modulos.externo.dominio.repositorios import RepositorioPublicaciones
from alpespartners.seedwork.aplicacion.comandos import Comando
from alpespartners.modulos.externo.aplicacion.dto import PublicacionDTO
from .base import CrearPublicacionBaseHandler
from dataclasses import dataclass
from alpespartners.seedwork.aplicacion.comandos import ejecutar_commando as comando

from alpespartners.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from alpespartners.modulos.externo.aplicacion.mapeadores import MapeadorPlataforma, MapeadorPublicacion


@dataclass
class CrearPlataforma(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str



class CrearPlataformaHandler(CrearPublicacionBaseHandler):

    def handle(self, comando: CrearPlataforma):
        plataforma_dto = PublicacionDTO(
            fecha_actualizacion=comando.fecha_actualizacion,
            fecha_creacion=comando.fecha_creacion,
            id=comando.id,
            tipo_publicacion=comando.tipo_publicacion
        )

        plataforma: Plataforma = self.fabrica_publicaciones.crear_objeto(plataforma_dto, MapeadorPlataforma())
        plataforma.crear_plataforma(plataforma)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPublicaciones.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, plataforma)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearPlataforma)
def ejecutar_comando_crear_plataforma(comando: CrearPlataforma):
    handler = CrearPlataformaHandler()
    handler.handle(comando)
    