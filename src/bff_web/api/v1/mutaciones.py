import uuid
import strawberry
from bff_web.despachadores import Despachador
from .esquemas import CrearAsociacionInput, Respuesta

import utils

@strawberry.type
class Mutation:
    @strawberry.mutation
    def crearAsociacion(self, input: CrearAsociacionInput, id_usuario: str = "default_user", id_correlacion: str = str(uuid.uuid4())) -> Respuesta:
        payload = dict(
            id_usuario=id_usuario,
            id_correlacion=id_correlacion,
            id_marca=input.id_marca,
            id_socio=input.id_socio,
            tipo=input.tipo,
            descripcion=input.descripcion,
            fecha_inicio=input.vigencia.fecha_inicio if input.vigencia else None,
            fecha_fin=input.vigencia.fecha_fin if input.vigencia else None,
        )
        
        comando = dict(
            id = str(uuid.uuid4()),
            time=utils.time_millis(),
            specversion="v1",
            type="CrearAsociacionEstrategica",
            ingestion=utils.time_millis(),
            datacontenttype="AVRO",
            service_name="BFF Web",
            data=payload,
        )
        
        despachador = Despachador()
        input.context["background_tasks"].add_task(despachador.publicar_mensaje, comando, "comando-crear-asociacion-estrategica", "public/default/comando-crear-asociacion-estrategica")

        return Respuesta(mensaje="Procesando Mensaje", codigo=203, idSolicitud=id_correlacion)

    