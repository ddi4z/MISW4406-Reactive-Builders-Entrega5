""" Fábricas para la creación de objetos en la capa de infraestructura 
del dominio de Asociaciones Estratégicas
"""

from dataclasses import dataclass
from asociaciones_estrategicas.seedwork.dominio.fabricas import Fabrica
from asociaciones_estrategicas.seedwork.dominio.repositorios import Repositorio
from asociaciones_estrategicas.seedwork.infraestructura.vistas import Vista

from asociaciones_estrategicas.modulos.asociaciones.dominio.entidades import AsociacionEstrategica
from asociaciones_estrategicas.modulos.asociaciones.dominio.repositorios import (
    RepositorioAsociacionEstrategica,
    RepositorioEventosAsociacionEstrategica,
)
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.repositorios import (
    RepositorioAsociacionesSQLAlchemy,
    RepositorioEventosAsociacionesSQLAlchemy,
)
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.vistas import VistaAsociacion
from .excepciones import ExcepcionFabrica


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioAsociacionEstrategica:
            return RepositorioAsociacionesSQLAlchemy()
        elif obj == RepositorioEventosAsociacionEstrategica:
            return RepositorioEventosAsociacionesSQLAlchemy()
        else:
            raise ExcepcionFabrica(f"No existe fábrica para el objeto {obj}")


@dataclass
class FabricaVista(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Vista:
        if obj == AsociacionEstrategica:
            return VistaAsociacion()
        else:
            raise ExcepcionFabrica(f"No existe fábrica para el objeto {obj}")
