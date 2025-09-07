""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass, field
from alpespartners.modulos.externo.infraestructura.repositorios import RepositorioEventosPostgres, RepositorioMediosMarketingPostgres, RepositorioPlataformasPostgres, RepositorioPublicacionesPostgres
from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.repositorios import Repositorio
from alpespartners.modulos.externo.dominio.repositorios import RepositorioEventos, RepositorioMediosMarketing, RepositorioPlataformas, RepositorioPublicaciones
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioEventos.__class__:
            return RepositorioEventosPostgres()
        elif obj == RepositorioPublicaciones.__class__:
            return RepositorioPublicacionesPostgres()
        elif obj == RepositorioPlataformas.__class__:
            return RepositorioPlataformasPostgres()
        elif obj == RepositorioMediosMarketing.__class__:
            return RepositorioMediosMarketingPostgres()
        else:
            raise ExcepcionFabrica()
        
        
