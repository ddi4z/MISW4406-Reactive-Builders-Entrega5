from alpespartners.modulos.eventos_medios.dominio.entidades import MedioMarketing, Publicacion
from alpespartners.modulos.eventos_medios.dominio.repositorios import RepositorioMediosMarketing, RepositorioPublicaciones
from alpespartners.seedwork.aplicacion.comandos import Comando
from alpespartners.modulos.eventos_medios.aplicacion.dto import PublicacionDTO
from alpespartners.seedwork.dominio.excepciones import ExcepcionDominio
from .base import CrearPublicacionBaseHandler
from dataclasses import dataclass
from alpespartners.seedwork.aplicacion.comandos import ejecutar_commando as comando

from alpespartners.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from alpespartners.modulos.eventos_medios.aplicacion.mapeadores import MapeadorPublicacion


@dataclass
class CrearPublicacion(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    id_medio_marketing: str
    tipo_publicacion: str


class CrearPublicacionHandler(CrearPublicacionBaseHandler):

      def handle(self, comando: CrearPublicacion):

        publicacion_dto = PublicacionDTO(
            fecha_actualizacion=comando.fecha_actualizacion,
            fecha_creacion=comando.fecha_creacion,
            id=comando.id,
            id_medio_marketing=comando.id_medio_marketing,
            tipo_publicacion=comando.tipo_publicacion
        )

        publicacion: Publicacion = self.fabrica_publicaciones.crear_objeto(publicacion_dto, MapeadorPublicacion())

        repo_medios = self.fabrica_repositorio.crear_objeto(RepositorioMediosMarketing)
        medio: MedioMarketing = repo_medios.obtener_por_id(comando.id_medio_marketing)

        if not medio:
            raise ExcepcionDominio(f"Medio de marketing {comando.id_medio_marketing} no encontrado")

        medio.crear_publicacion(publicacion)

        UnidadTrabajoPuerto.registrar_batch(repo_medios.agregar, medio)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearPublicacion)
def ejecutar_comando_crear_publicacion(comando: CrearPublicacion):
    handler = CrearPublicacionHandler()
    handler.handle(comando)
    