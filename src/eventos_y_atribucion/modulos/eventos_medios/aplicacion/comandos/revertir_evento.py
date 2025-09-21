from abc import ABC
from datetime import datetime
import logging
from eventos_y_atribucion.modulos.comision_recompensa.aplicacion.comandos.crear_comision import CrearComision
from eventos_y_atribucion.modulos.comision_recompensa.aplicacion.comandos.crear_recompensa import CrearRecompensa
from eventos_y_atribucion.modulos.eventos_medios.dominio.entidades import Evento, Lead
from eventos_y_atribucion.modulos.eventos_medios.aplicacion.dto import EventoDTO
from eventos_y_atribucion.modulos.eventos_medios.dominio.eventos import EventoCancelado
from eventos_y_atribucion.modulos.eventos_medios.dominio.repositorios import RepositorioEventos, RepositorioEventosEventos
from eventos_y_atribucion.seedwork.aplicacion.comandos import Comando, ejecutar_commando
from .base import CrearEventoBaseHandler, CrearPublicacionBaseHandler
from dataclasses import dataclass
from eventos_y_atribucion.seedwork.aplicacion.comandos import ejecutar_commando as comando

from eventos_y_atribucion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from eventos_y_atribucion.modulos.eventos_medios.aplicacion.mapeadores import MapeadorEvento


@dataclass
class RevertirEvento(Comando):
    id_correlacion: str
    id_evento: str
    fecha_creacion: str
    fecha_actualizacion: str
    motivo: str = ""


class RevertirEventoHandler(CrearEventoBaseHandler):

    def handle(self, comando: RevertirEvento):        
        agregada = Evento()
        agregada.agregar_evento(EventoCancelado(
            id_correlacion=comando.id_correlacion,
            id_evento=comando.id_evento,
            motivo=comando.motivo,
            fecha_cancelacion=datetime.now()
        ))


        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEventos)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(
            RepositorioEventosEventos
        )
        
        UnidadTrabajoPuerto.registrar_batch(
            repositorio.revertir, comando.id_evento
        )

        UnidadTrabajoPuerto.registrar_batch(
            lambda x: None,
            agregada,
            repositorio_eventos_func=repositorio_eventos.agregar,
        )
        
        UnidadTrabajoPuerto.commit()
        logging.info(f"[SAGA] EventoCancelado emitido (corr={comando.id_correlacion}, id={comando.id_evento})")


@comando.register(RevertirEvento)
def ejecutar_comando_revertir_evento(comando: RevertirEvento):
    handler = RevertirEventoHandler()
    handler.handle(comando)
    
