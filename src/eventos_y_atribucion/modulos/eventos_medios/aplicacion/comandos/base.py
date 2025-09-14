from eventos_y_atribucion.seedwork.aplicacion.comandos import ComandoHandler
from eventos_y_atribucion.modulos.eventos_medios.infraestructura.fabricas import FabricaRepositorio
from eventos_y_atribucion.modulos.eventos_medios.dominio.fabricas import FabricaEventos, FabricaMediosMarketing, FabricaPublicaciones

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
    
class CrearMedioMarketingBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_medios_marketing: FabricaMediosMarketing = FabricaMediosMarketing()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_medios_marketing(self):
        return self._fabrica_medios_marketing
    
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
