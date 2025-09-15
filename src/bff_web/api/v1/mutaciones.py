import strawberry
from .esquemas import CrearAsociacionInput, Respuesta, crear_asociacion

@strawberry.type
class Mutation:
    @strawberry.mutation
    def crearAsociacion(self, input: CrearAsociacionInput) -> Respuesta:
        payload = {
            "id_marca": input.id_marca,
            "id_socio": input.id_socio,
            "tipo": input.tipo,
            "descripcion": input.descripcion,
            "vigencia": (
                {
                    "fecha_inicio": input.vigencia.fecha_inicio,
                    "fecha_fin": input.vigencia.fecha_fin
                } if input.vigencia else None
            )
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        return crear_asociacion(payload)

