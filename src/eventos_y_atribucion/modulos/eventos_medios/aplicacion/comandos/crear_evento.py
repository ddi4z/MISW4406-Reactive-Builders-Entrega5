from abc import ABC
import logging
from eventos_y_atribucion.modulos.comision_recompensa.aplicacion.comandos.crear_comision import CrearComision
from eventos_y_atribucion.modulos.comision_recompensa.aplicacion.comandos.crear_recompensa import CrearRecompensa
from eventos_y_atribucion.modulos.eventos_medios.dominio.entidades import Evento, Lead
from eventos_y_atribucion.modulos.eventos_medios.aplicacion.dto import EventoDTO
from eventos_y_atribucion.modulos.eventos_medios.dominio.eventos import EventoFallido
from eventos_y_atribucion.modulos.eventos_medios.dominio.repositorios import RepositorioEventos, RepositorioEventosEventos
from eventos_y_atribucion.seedwork.aplicacion.comandos import Comando, ejecutar_commando
from .base import CrearEventoBaseHandler, CrearPublicacionBaseHandler
from dataclasses import dataclass
from eventos_y_atribucion.seedwork.aplicacion.comandos import ejecutar_commando as comando

from eventos_y_atribucion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from eventos_y_atribucion.modulos.eventos_medios.aplicacion.mapeadores import MapeadorEvento


@dataclass
class CrearEvento(Comando):
    id_correlacion: str
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    tipo_evento:str
    id_publicacion:str


class CrearEventoHandler(CrearEventoBaseHandler):

    def handle(self, comando: CrearEvento):
        try:
            evento_dto = EventoDTO(
                tipo_evento=comando.tipo_evento,
                id_publicacion = comando.id_publicacion
            )

            evento: Evento = self.fabrica_eventos.crear_objeto(evento_dto, MapeadorEvento())
            evento.crear_evento(evento)
            repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEventos)
            repositorio_eventos = self.fabrica_repositorio.crear_objeto(
                RepositorioEventosEventos
            )
            
            UnidadTrabajoPuerto.registrar_batch(
                repositorio.agregar,
                evento,
                repositorio_eventos_func=repositorio_eventos.agregar,
            )
            UnidadTrabajoPuerto.commit()
            
            if isinstance(evento, Lead):
                comando = CrearComision(evento.fecha_creacion.strftime("%Y-%m-%dT%H:%M:%SZ"), evento.fecha_actualizacion.strftime("%Y-%m-%dT%H:%M:%SZ"), evento.id, evento.id)
                ejecutar_commando(comando)
            else:
                comando = CrearRecompensa(evento.fecha_creacion.strftime("%Y-%m-%dT%H:%M:%SZ"), evento.fecha_actualizacion.strftime("%Y-%m-%dT%H:%M:%SZ"), evento.id, evento.id)
                ejecutar_commando(comando)
        except Exception as e:
            print(f"Procesando la exepcion dentro del handler {e}")
            logging.warning(f"[SAGA] EventoFallido emitido: {str(e)} (id_correlacion={comando.id_correlacion})")

            evento = Evento()
            evento.agregar_evento(EventoFallido(
                id_correlacion=comando.id_correlacion,
                id_evento=comando.id,
                motivo=str(e),
            ))

            repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosEventos)

            UnidadTrabajoPuerto.registrar_batch(
                lambda x: None,
                evento,
                repositorio_eventos_func=repositorio_eventos.agregar,
            )
            UnidadTrabajoPuerto.commit()
  


@comando.register(CrearEvento)
def ejecutar_comando_crear_evento(comando: CrearEvento):
    handler = CrearEventoHandler()
    handler.handle(comando)
    