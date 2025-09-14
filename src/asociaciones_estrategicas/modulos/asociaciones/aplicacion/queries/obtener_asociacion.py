from dataclasses import dataclass
import uuid

from asociaciones_estrategicas.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from asociaciones_estrategicas.seedwork.aplicacion.queries import ejecutar_query as query

from asociaciones_estrategicas.modulos.asociaciones.dominio.entidades import AsociacionEstrategica
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.mapeadores import MapeadorAsociacion
from .base import AsociacionQueryBaseHandler


# ==========
# Query
# ==========

@dataclass
class ObtenerAsociacion(Query):
    id: str


# ==========
# Handler
# ==========

class ObtenerAsociacionHandler(AsociacionQueryBaseHandler):

    def handle(self, query: ObtenerAsociacion) -> QueryResultado:
        vista = self.fabrica_vista.crear_objeto(AsociacionEstrategica)
        asociaciones = vista.obtener_por(query.id)

        if not asociaciones:
            return QueryResultado(resultado=None)

        asociacion = self.fabrica_asociaciones.crear_objeto(
            asociaciones[0], MapeadorAsociacion()
        )
        return QueryResultado(resultado=asociacion)
# ==========
# Registro
# ==========

@query.register(ObtenerAsociacion)
def ejecutar_query_obtener_asociacion(query: ObtenerAsociacion):
    handler = ObtenerAsociacionHandler()
    return handler.handle(query)    