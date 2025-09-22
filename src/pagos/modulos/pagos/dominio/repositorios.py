""" Interfaces para los repositorios del dominio de vuelos

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de vuelos

"""

from abc import ABC, abstractmethod
from pagos.seedwork.dominio.repositorios import Repositorio

class RepositorioPagos(Repositorio, ABC):
    @abstractmethod
    def revertir(self, entity_id):
        ...
    
class RepositorioEventosPagos(Repositorio, ABC):
    ...
    
