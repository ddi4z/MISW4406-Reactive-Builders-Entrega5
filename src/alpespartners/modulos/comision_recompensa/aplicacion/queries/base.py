from alpespartners.seedwork.aplicacion.queries import QueryHandler
from alpespartners.modulos.comision_recompensa.infraestructura.fabricas import FabricaRepositorio
from alpespartners.modulos.comision_recompensa.dominio.fabricas import FabricaEventos

class EventoQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_eventos: FabricaEventos = FabricaEventos()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_eventos(self):
        return self._fabrica_eventos