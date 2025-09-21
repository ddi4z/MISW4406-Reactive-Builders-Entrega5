""" Interfaces para los repositorios del dominio de vuelos

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de vuelos

"""

from abc import ABC, abstractmethod
from uuid import UUID
from eventos_y_atribucion.seedwork.dominio.repositorios import Repositorio

class RepositorioEventos(Repositorio, ABC):
    @abstractmethod
    def revertir(self, entity_id: UUID):
        ...


class RepositorioMediosMarketing(Repositorio, ABC):
    ...
    
class RepositorioEventosEventos(Repositorio, ABC):
    ...