from dataclasses import dataclass
from asociaciones_estrategicas.seedwork.aplicacion.queries import Query, QueryResultado, ejecutar_query as query
from .base import AsociacionQueryBaseHandler
from asociaciones_estrategicas.modulos.asociaciones.dominio.entidades import AsociacionEstrategica

@dataclass
class ObtenerAsociaciones(Query):
    id_asociacion: str = None
    id_marca: str = None
    id_socio: str = None
    tipo: str = None

class ObtenerAsociacionesHandler(AsociacionQueryBaseHandler):
    def handle(self, query: ObtenerAsociaciones) -> QueryResultado:
        vista = self.fabrica_vista.crear_objeto(AsociacionEstrategica)
        asociaciones = vista.obtener_por(
            id_asociacion=query.id_asociacion,
            id_marca=query.id_marca,
            id_socio=query.id_socio,
            tipo=query.tipo,
        )
        return QueryResultado(resultado=asociaciones)

@query.register(ObtenerAsociaciones)
def ejecutar_query_obtener_asociaciones(query: ObtenerAsociaciones):
    handler = ObtenerAsociacionesHandler()
    return handler.handle(query)
