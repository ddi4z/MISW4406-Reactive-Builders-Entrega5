from asociaciones_estrategicas.seedwork.aplicacion.comandos import ComandoHandler
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.fabricas import FabricaRepositorio
from asociaciones_estrategicas.modulos.asociaciones.dominio.fabricas import FabricaAsociacionesEstrategicas

class CrearAsociacionBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_asociaciones: FabricaAsociacionesEstrategicas = FabricaAsociacionesEstrategicas()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_asociaciones(self):
        return self._fabrica_asociaciones
