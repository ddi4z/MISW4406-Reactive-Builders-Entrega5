import strawberry
from typing import List
from .esquemas import (
    Asociacion,
    obtener_asociaciones,
    obtener_asociacion,
    obtener_asociaciones_por_marca,
)

@strawberry.type
class Query:
    @strawberry.field
    def asociaciones(self) -> List[Asociacion]:
        return obtener_asociaciones()

    @strawberry.field
    def asociacion(self, id: str) -> Asociacion:
        return obtener_asociacion(id)

    @strawberry.field
    def asociacionesPorMarca(self, idMarca: str) -> List[Asociacion]:
        return obtener_asociaciones_por_marca(idMarca)
