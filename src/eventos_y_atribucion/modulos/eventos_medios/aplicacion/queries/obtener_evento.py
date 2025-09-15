from eventos_y_atribucion.modulos.eventos_medios.infraestructura.repositorios import RepositorioEventos
from eventos_y_atribucion.seedwork.aplicacion.queries import Query, QueryResultado
from eventos_y_atribucion.seedwork.aplicacion.queries import ejecutar_query as query
from dataclasses import dataclass
from .base import EventoQueryBaseHandler
from eventos_y_atribucion.modulos.eventos_medios.aplicacion.mapeadores import MapeadorEvento
import uuid
from typing import Optional

@dataclass
class ObtenerEvento(Query):
    id: Optional[str]

class ObtenerEventoHandler(EventoQueryBaseHandler):

    def handle(self, query: ObtenerEvento) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEventos)
        if query.id:
            return QueryResultado(resultado=self.fabrica_eventos.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorEvento()))
        return QueryResultado(resultado=[self.fabrica_eventos.crear_objeto(evento, MapeadorEvento()) for evento in repositorio.obtener_todos()])

@query.register(ObtenerEvento)
def ejecutar_query_obtener_evento(query: ObtenerEvento):
    handler = ObtenerEventoHandler()
    return handler.handle(query)