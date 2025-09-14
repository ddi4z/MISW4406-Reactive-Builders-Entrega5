from abc import ABC
from eventos_y_atribucion.modulos.comision_recompensa.aplicacion.comandos.crear_comision import CrearComision
from eventos_y_atribucion.modulos.comision_recompensa.aplicacion.comandos.crear_recompensa import CrearRecompensa
from eventos_y_atribucion.modulos.eventos_medios.dominio.entidades import Evento, Lead
from eventos_y_atribucion.modulos.eventos_medios.aplicacion.dto import EventoDTO
from eventos_y_atribucion.modulos.eventos_medios.dominio.repositorios import RepositorioEventos
from eventos_y_atribucion.seedwork.aplicacion.comandos import Comando, ejecutar_commando
from .base import CrearEventoBaseHandler, CrearPublicacionBaseHandler
from dataclasses import dataclass
from eventos_y_atribucion.seedwork.aplicacion.comandos import ejecutar_commando as comando

from eventos_y_atribucion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from eventos_y_atribucion.modulos.eventos_medios.aplicacion.mapeadores import MapeadorEvento


@dataclass
class CrearEvento(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    tipo_evento:str
    id_publicacion:str


class CrearEventoHandler(CrearEventoBaseHandler):

    def handle(self, comando: CrearEvento):
        evento_dto = EventoDTO(
            fecha_actualizacion=comando.fecha_actualizacion,
            fecha_creacion=comando.fecha_creacion,
            id=comando.id,
            tipo_evento=comando.tipo_evento,
            id_publicacion = comando.id_publicacion
        )

        evento: Evento = self.fabrica_eventos.crear_objeto(evento_dto, MapeadorEvento())
        evento.crear_evento(evento)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEventos)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, evento)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()
        
        if isinstance(evento, Lead):
            comando = CrearComision(evento.fecha_creacion.strftime("%Y-%m-%dT%H:%M:%SZ"), evento.fecha_actualizacion.strftime("%Y-%m-%dT%H:%M:%SZ"), evento.id, evento.id)
            ejecutar_commando(comando)
        else:
            comando = CrearRecompensa(evento.fecha_creacion.strftime("%Y-%m-%dT%H:%M:%SZ"), evento.fecha_actualizacion.strftime("%Y-%m-%dT%H:%M:%SZ"), evento.id, evento.id)
            ejecutar_commando(comando)


@comando.register(CrearEvento)
def ejecutar_comando_crear_evento(comando: CrearEvento):
    handler = CrearEventoHandler()
    handler.handle(comando)
    