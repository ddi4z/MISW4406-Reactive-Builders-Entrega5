""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import AsociacionEstrategica
from .reglas import FechaInicioDebeSerAnteriorFin
from .excepciones import TipoObjetoNoExisteEnDominioAsociacionesEstrategicasExcepcion
from asociaciones_estrategicas.seedwork.dominio.repositorios import Mapeador, Repositorio
from asociaciones_estrategicas.seedwork.dominio.fabricas import Fabrica
from asociaciones_estrategicas.seedwork.dominio.entidades import Entidad
from asociaciones_estrategicas.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

##Fábrica para la creación de asociaciones estratégicas
@dataclass
class _FabricaAsociacionEstrategica(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            asociacion_estrategica: AsociacionEstrategica = mapeador.dto_a_entidad(obj)
            self.validar_regla(FechaInicioDebeSerAnteriorFin(asociacion_estrategica.vigencia))

            return asociacion_estrategica

##Fabrica principal expuesta por el módulo
@dataclass
class FabricaAsociacionesEstrategicas(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == AsociacionEstrategica.__class__:
            fabrica_asociacion_estrategica = _FabricaAsociacionEstrategica()
            return fabrica_asociacion_estrategica.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioAsociacionesEstrategicasExcepcion()

