from aeroalpes.modulos.externo.dominio.entidades import Evento
from aeroalpes.modulos.externo.aplicacion.dto import EventoDTO
from aeroalpes.modulos.externo.dominio.repositorios import RepositorioEventos
from aeroalpes.seedwork.aplicacion.comandos import Comando
from .base import CrearPublicacionBaseHandler
from dataclasses import dataclass
from aeroalpes.seedwork.aplicacion.comandos import ejecutar_commando as comando

from aeroalpes.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from aeroalpes.modulos.externo.aplicacion.mapeadores import MapeadorEvento


@dataclass
class CrearEvento(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str


class CrearEventoHandler(CrearPublicacionBaseHandler):

    def handle(self, comando: CrearEvento):
        evento_dto = EventoDTO(
            fecha_actualizacion=comando.fecha_actualizacion,
            fecha_creacion=comando.fecha_creacion,
            id=comando.id,
            itinerarios=comando.itinerarios
        )

        evento: Evento = self.fabrica_eventos.crear_objeto(evento_dto, MapeadorEvento())
        evento.crear_evento(evento)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEventos.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, evento)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearEvento)
def ejecutar_comando_crear_evento(comando: CrearEvento):
    handler = CrearEventoHandler()
    handler.handle(comando)
    