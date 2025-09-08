"""Objetos valor del dominio de vuelos

En este archivo usted encontrará los objetos valor del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass
from alpespartners.seedwork.dominio.objetos_valor import ObjetoValor


@dataclass(frozen=True)
class MontoComision(ObjetoValor):
    valor: int