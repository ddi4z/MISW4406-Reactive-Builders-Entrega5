from alpespartners.seedwork.aplicacion.queries import QueryHandler
from alpespartners.modulos.externo.infraestructura.fabricas import FabricaRepositorio
from alpespartners.modulos.externo.dominio.fabricas import FabricaVuelos

class ReservaQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_vuelos: FabricaVuelos = FabricaVuelos()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_vuelos(self):
        return self._fabrica_vuelos    