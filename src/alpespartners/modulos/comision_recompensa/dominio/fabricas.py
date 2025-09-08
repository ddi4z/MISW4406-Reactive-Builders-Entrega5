""" Fábricas para la creación de objetos del dominio de publicaciones y eventos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de publicaciones y eventos

"""

from .entidades import Comision, Recompensa
from .excepciones import TipoObjetoNoExisteEnDominioVuelosExcepcion
from alpespartners.seedwork.dominio.repositorios import Mapeador
from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass



@dataclass
class FabricaComisiones(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Comision.__class__:
            if isinstance(obj, Entidad):
                return mapeador.entidad_a_dto(obj)
            else:
                comision: Comision = mapeador.dto_a_entidad(obj)
                return comision
        else:
            raise TipoObjetoNoExisteEnDominioVuelosExcepcion()
        
@dataclass
class FabricaRecompensas(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Recompensa.__class__:
            if isinstance(obj, Entidad):
                return mapeador.entidad_a_dto(obj)
            else:
                recompensa: Recompensa = mapeador.dto_a_entidad(obj)
                return recompensa
        else:
            raise TipoObjetoNoExisteEnDominioVuelosExcepcion()