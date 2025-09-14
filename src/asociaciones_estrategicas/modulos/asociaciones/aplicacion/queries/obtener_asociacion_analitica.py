# modulos/asociaciones/aplicacion/queries/obtener_analitica_asociaciones.py
from dataclasses import dataclass
from asociaciones_estrategicas.seedwork.aplicacion.queries import Query, QueryResultado, ejecutar_query as query
from .base import AsociacionQueryBaseHandler
from asociaciones_estrategicas.modulos.asociaciones.dominio.entidades import AsociacionEstrategica

@dataclass
class ObtenerAnaliticaAsociaciones(Query):
    pass

class ObtenerAnaliticaAsociacionesHandler(AsociacionQueryBaseHandler):
    def handle(self, query: ObtenerAnaliticaAsociaciones) -> QueryResultado:
        vista = self.fabrica_vista.crear_objeto("Analitica")
        analitica = vista.obtener_por()   
        return QueryResultado(resultado=analitica)

@query.register(ObtenerAnaliticaAsociaciones)
def ejecutar_query_obtener_analitica(query: ObtenerAnaliticaAsociaciones):
    handler = ObtenerAnaliticaAsociacionesHandler()
    return handler.handle(query)
