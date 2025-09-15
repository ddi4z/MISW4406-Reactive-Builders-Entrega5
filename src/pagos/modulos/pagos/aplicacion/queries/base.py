from pagos.seedwork.aplicacion.queries import QueryHandler
from pagos.modulos.pagos.infraestructura.fabricas import FabricaRepositorio
from pagos.modulos.pagos.dominio.fabricas import FabricaPagos

class PagoComisionQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_pagos: FabricaPagos = FabricaPagos()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_pagos(self):
        return self._fabrica_pagos