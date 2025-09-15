from pagos.modulos.pagos.infraestructura.repositorios import RepositorioPagos
from pagos.seedwork.aplicacion.queries import Query, QueryResultado
from pagos.seedwork.aplicacion.queries import ejecutar_query as query
from dataclasses import dataclass
from .base import PagoComisionQueryBaseHandler
from pagos.modulos.pagos.aplicacion.mapeadores import MapeadorPago

@dataclass
class ObtenerPagoComision(Query):
    id: str | None

class ObtenerPagoComisionHandler(PagoComisionQueryBaseHandler):

    def handle(self, query: ObtenerPagoComision) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPagos)
        if query.id:
            return QueryResultado(resultado=self.fabrica_pagos.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorPago()))
        return QueryResultado(resultado=[self.fabrica_pagos.crear_objeto(pago, MapeadorPago()) for pago in repositorio.obtener_todos()])

@query.register(ObtenerPagoComision)
def ejecutar_query_obtener_pago_comision(query: ObtenerPagoComision):
    handler = ObtenerPagoComisionHandler()
    return handler.handle(query)