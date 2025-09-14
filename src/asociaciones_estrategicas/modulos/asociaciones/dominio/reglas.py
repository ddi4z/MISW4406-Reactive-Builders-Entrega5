"""Reglas de negocio del dominio de cliente

En este archivo usted encontrará reglas de negocio del dominio de cliente

"""

from asociaciones_estrategicas.seedwork.dominio.reglas import ReglaNegocio
from .objetos_valor import PeriodoVigencia


class FechaInicioDebeSerAnteriorFin(ReglaNegocio):

    def __init__(self, vigencia: PeriodoVigencia, mensaje="La fecha de inicio debe ser anterior a la fecha de fin"):
        super().__init__(mensaje)
        self.vigencia = vigencia

    def es_valido(self) -> bool:
        return self.vigencia.fecha_inicio < self.vigencia.fecha_fin