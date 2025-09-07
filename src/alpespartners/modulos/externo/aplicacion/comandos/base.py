from alpespartners.seedwork.aplicacion.comandos import ComandoHandler
from alpespartners.modulos.externo.infraestructura.fabricas import FabricaRepositorio
from alpespartners.modulos.externo.dominio.fabricas import FabricaEventos, FabricaPublicaciones

class CrearPublicacionBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_publicaciones: FabricaPublicaciones = FabricaPublicaciones()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_publicaciones(self):
        return self._fabrica_publicaciones
    
class CrearEventoBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_eventos: FabricaEventos = FabricaEventos()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_eventos(self):
        return self._fabrica_eventos
