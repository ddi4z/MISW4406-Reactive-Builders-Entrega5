""" Interfaces para los repositorios del dominio de Respositorios

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de Asociaciones Estrategicas

"""

from abc import ABC
from asociaciones_estrategicas.seedwork.dominio.repositorios import Repositorio

class RepositorioAsociacionEstrategica(Repositorio, ABC):
    ...

class RepositorioEventosAsociacionEstrategica(Repositorio, ABC):
    ...
