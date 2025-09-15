""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass
from pagos.modulos.pagos.dominio.repositorios import RepositorioPagos
from pagos.modulos.pagos.infraestructura.repositorios import RepositorioPagosPostgres
from pagos.seedwork.dominio.fabricas import Fabrica
from pagos.seedwork.dominio.repositorios import Repositorio
from .excepciones import ExcepcionFabrica

@dataclass
@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if issubclass(obj, RepositorioPagos):
            return RepositorioPagosPostgres()
        else:
            raise ExcepcionFabrica(f"No se reconoce el repositorio para {obj}")

        
        
