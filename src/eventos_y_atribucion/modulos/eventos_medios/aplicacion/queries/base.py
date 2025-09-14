from eventos_y_atribucion.seedwork.aplicacion.queries import QueryHandler
from eventos_y_atribucion.modulos.eventos_medios.infraestructura.fabricas import FabricaRepositorio
from eventos_y_atribucion.modulos.eventos_medios.dominio.fabricas import FabricaEventos

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