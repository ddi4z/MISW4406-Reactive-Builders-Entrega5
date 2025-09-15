""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass, field
from .repositorios import RepositorioComisiones, RepositorioRecompensas
from eventos_y_atribucion.modulos.comision_recompensa.infraestructura.repositorios import RepositorioRecompensasPostgres, RepositorioComisionesPostgres
from eventos_y_atribucion.seedwork.dominio.fabricas import Fabrica
from eventos_y_atribucion.seedwork.dominio.repositorios import Repositorio
from .excepciones import ExcepcionFabrica

@dataclass
@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if issubclass(obj, RepositorioRecompensas):
            return RepositorioRecompensasPostgres()
        elif issubclass(obj, RepositorioComisiones):
            return RepositorioComisionesPostgres()
        else:
            raise ExcepcionFabrica(f"No se reconoce el repositorio para {obj}")

        
        
