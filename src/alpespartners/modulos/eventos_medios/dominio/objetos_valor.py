"""Objetos valor del dominio de vuelos

En este archivo usted encontrará los objetos valor del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from alpespartners.seedwork.dominio.objetos_valor import ObjetoValor

class TipoPublicacion(Enum):
    ...
    
@dataclass(frozen=True)
class Plataforma(ObjetoValor):
    nombre: str