""" Fábricas para la creación de objetos del dominio de publicaciones y eventos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de publicaciones y eventos

"""

from .entidades import Evento, MedioMarketing, Publicacion
from .excepciones import TipoObjetoNoExisteEnDominioVuelosExcepcion
from alpespartners.seedwork.dominio.repositorios import Mapeador
from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass



@dataclass
class FabricaPublicaciones(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Publicacion.__class__:
            if isinstance(obj, Entidad):
                return mapeador.entidad_a_dto(obj)
            else:
                publicacion: Publicacion = mapeador.dto_a_entidad(obj)
                return publicacion
        else:
            raise TipoObjetoNoExisteEnDominioVuelosExcepcion()
        
@dataclass
class FabricaEventos(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Evento.__class__:
            if isinstance(obj, Entidad):
                return mapeador.entidad_a_dto(obj)
            else:
                evento: Evento = mapeador.dto_a_entidad(obj)
                return evento
        else:
            raise TipoObjetoNoExisteEnDominioVuelosExcepcion()
        
@dataclass
class FabricaMediosMarketing(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        print()
        if mapeador.obtener_tipo() == MedioMarketing.__class__:
            if isinstance(obj, Entidad):
                return mapeador.entidad_a_dto(obj)
            else:
                medio_marketing: MedioMarketing = mapeador.dto_a_entidad(obj)
                return medio_marketing
        else:
            raise TipoObjetoNoExisteEnDominioVuelosExcepcion()