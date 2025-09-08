from alpespartners.modulos.comision_recompensa.infraestructura.repositorios import RepositorioEventos
from alpespartners.seedwork.aplicacion.queries import Query, QueryResultado
from alpespartners.seedwork.aplicacion.queries import ejecutar_query as query
from dataclasses import dataclass
from .base import EventoQueryBaseHandler
from alpespartners.modulos.comision_recompensa.aplicacion.mapeadores import MapeadorEvento
import uuid

@dataclass
class ObtenerEvento(Query):
    id: str | None

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