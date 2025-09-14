from dataclasses import dataclass
import uuid

from asociaciones_estrategicas.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from asociaciones_estrategicas.seedwork.aplicacion.queries import ejecutar_query as query

from asociaciones_estrategicas.modulos.asociaciones.dominio.entidades import AsociacionEstrategica
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.mapeadores import MapeadorAsociacion
from .base import AsociacionQueryBaseHandler



@dataclass
class ObtenerAsociacionesPorMarca(Query):
    id_marca: str

class ObtenerAsociacionesPorMarcaHandler(AsociacionQueryBaseHandler):
    def handle(self, query: ObtenerAsociacionesPorMarca) -> QueryResultado:
        vista = self.fabrica_vista.crear_objeto(AsociacionEstrategica)
        asociaciones = vista.obtener_por(id_marca=query.id_marca)
        return QueryResultado(resultado=asociaciones)

@query.register(ObtenerAsociacionesPorMarca)
def ejecutar_query_obtener_asociaciones_por_marca(query: ObtenerAsociacionesPorMarca):
    handler = ObtenerAsociacionesPorMarcaHandler()
    return handler.handle(query)



