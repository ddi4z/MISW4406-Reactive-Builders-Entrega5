"""Objetos valor del dominio de vuelos

En este archivo usted encontrará los objetos valor del dominio de vuelos

"""

from __future__ import annotations

from dataclasses import dataclass, field
from asociaciones_estrategicas.seedwork.dominio.objetos_valor import ObjetoValor, Codigo, Ruta, Locacion
from datetime import datetime
from enum import Enum

class TipoAsociacion(Enum):
    PROGRAMA_AFILIADOS = "programa_afiliados"
    COLABORACION_DIRECTA = "colaboracion_directa"
    CAMPANIA = "campania"
    PROGRAMA_LEALTAD = "programa_lealtad"
    ALIANZA_B2B = "alianza_b2b"

@dataclass(frozen=True)
class PeriodoVigencia(ObjetoValor):
    fecha_inicio: datetime
    fecha_fin: datetime