from alpespartners.seedwork.aplicacion.comandos import ComandoHandler
from alpespartners.modulos.comision_recompensa.infraestructura.fabricas import FabricaRepositorio
from alpespartners.modulos.comision_recompensa.dominio.fabricas import FabricaComisiones, FabricaRecompensas

class CrearComisionBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_comisiones: FabricaComisiones = FabricaComisiones()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_comisiones(self):
        return self._fabrica_comisiones
    
class CrearRecompensaBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_recompensas: FabricaRecompensas = FabricaRecompensas()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_recompensas(self):
        return self._fabrica_recompensas
    