""" Fábricas para la creación de objetos del dominio de publicaciones y eventos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de publicaciones y eventos

"""

from pagos.seedwork.dominio.eventos import EventoDominio
from .entidades import Pago
from .excepciones import TipoObjetoNoExisteEnDominioPagosExcepcion
from pagos.seedwork.dominio.repositorios import Mapeador
from pagos.seedwork.dominio.fabricas import Fabrica
from pagos.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass



@dataclass
class FabricaPagos(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            return mapeador.dto_a_entidad(obj)

