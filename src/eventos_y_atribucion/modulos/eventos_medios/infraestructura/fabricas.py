""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass, field
from eventos_y_atribucion.modulos.eventos_medios.dominio.repositorios import RepositorioEventosEventos
from eventos_y_atribucion.modulos.eventos_medios.infraestructura.repositorios import RepositorioEventosPostgres, RepositorioMediosMarketingPostgres
from eventos_y_atribucion.seedwork.dominio.fabricas import Fabrica
from eventos_y_atribucion.seedwork.dominio.repositorios import Repositorio
from .repositorios import RepositorioEventos, RepositorioEventosEventosPostgres, RepositorioMediosMarketing
from .excepciones import ExcepcionFabrica

@dataclass
@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if issubclass(obj, RepositorioEventos):
            return RepositorioEventosPostgres()
        elif issubclass(obj, RepositorioMediosMarketing):
            return RepositorioMediosMarketingPostgres()
        elif issubclass(obj, RepositorioEventosEventos):
            return RepositorioEventosEventosPostgres()
        else:
            raise ExcepcionFabrica(f"No se reconoce el repositorio para {obj}")

        
        
