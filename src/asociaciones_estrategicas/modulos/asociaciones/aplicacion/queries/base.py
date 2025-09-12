from asociaciones_estrategicas.seedwork.aplicacion.queries import QueryHandler
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.fabricas import FabricaVista
from asociaciones_estrategicas.modulos.asociaciones.dominio.fabricas import FabricaAsociacionesEstrategicas

class AsociacionQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_vista: FabricaVista = FabricaVista()
        self._fabrica_asociaciones: FabricaAsociacionesEstrategicas = FabricaAsociacionesEstrategicas()

    @property
    def fabrica_vista(self):
        return self._fabrica_vista
    
    @property
    def fabrica_asociaciones(self):
        return self._fabrica_asociaciones
