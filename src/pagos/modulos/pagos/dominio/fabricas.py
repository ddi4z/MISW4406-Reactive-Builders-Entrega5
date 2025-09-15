""" Fábricas para la creación de objetos del dominio de publicaciones y eventos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de publicaciones y eventos

"""

from .entidades import Pago
from .excepciones import TipoObjetoNoExisteEnDominioPagosExcepcion
from pagos.seedwork.dominio.repositorios import Mapeador
from pagos.seedwork.dominio.fabricas import Fabrica
from pagos.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass



@dataclass
class FabricaPagos(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Pago:
            if isinstance(obj, Entidad):
                return mapeador.entidad_a_dto(obj)
            else:
                pago: Pago = mapeador.dto_a_entidad(obj)
                return pago
        else:
            raise TipoObjetoNoExisteEnDominioPagosExcepcion()
        
