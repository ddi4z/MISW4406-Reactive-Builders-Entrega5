from asociaciones_estrategicas.modulos.asociaciones.infraestructura.schema.v1.comandos import (
    ComandoCancelarAsociacionEstrategica, ComandoCancelarAsociacionPayload, ComandoIniciarTracking, ComandoIniciarTrackingPayload
)
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.despachadores import Despachador
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.schema.v1.comandos import (
    ComandoCrearAsociacionEstrategica, ComandoCrearAsociacionEstrategicaPayload
)
from pulsar.schema import AvroSchema

class ServicioTracking:
    def iniciar_tracking(self, asociacion):
        payload = ComandoIniciarTrackingPayload(
            id_asociacion_estrategica=str(asociacion.id),
            id_marca=str(asociacion.id_marca),
            id_socio=str(asociacion.id_socio),
            tipo=asociacion.tipo.value
        )
        comando = ComandoIniciarTracking(
            type="IniciarTracking",   
            data=payload
        )

        despachador = Despachador()
        despachador.publicar_comando(comando, "comandos-eventos_y_atribucion.iniciar_tracking")


class ServicioAsociacion:
    def crear_asociacion(self, asociacion_dto,in_id_correlacion: str):
        payload = ComandoCrearAsociacionEstrategicaPayload(
            #id_usuario="",  # opcional, podrías pasarlo desde la sesión
            id_correlacion=in_id_correlacion,
            id_marca=asociacion_dto.id_marca,
            id_socio=asociacion_dto.id_socio,
            tipo=asociacion_dto.tipo,
            descripcion=asociacion_dto.descripcion,
            fecha_inicio=asociacion_dto.vigencia.fecha_inicio,
            fecha_fin=asociacion_dto.vigencia.fecha_fin,
        )

        comando = ComandoCrearAsociacionEstrategica(
            type="CrearAsociacionEstrategica",
            specversion="v1",
            datacontenttype="AVRO",
            service_name="api-asociaciones",
            data=payload,
        )

        despachador = Despachador()
        despachador.publicar_comando(
            comando,
            topico="comandos-asociaciones.crear_asociacion",
            schema=AvroSchema(ComandoCrearAsociacionEstrategica),
        )

    def cancelar_asociacion(self, id_asociacion:str, motivo:str,in_id_correlacion: str):
        payload = ComandoCancelarAsociacionPayload(
            id_correlacion=in_id_correlacion,
            id_asociacion=id_asociacion,
            motivo=motivo
        )

        comando = ComandoCancelarAsociacionEstrategica(
            type="CancelarAsociacionEstrategica",
            specversion="v1",
            datacontenttype="AVRO",
            service_name="api-asociaciones",
            data=payload,
        )

        despachador = Despachador()
        despachador.publicar_comando(
            comando,
            topico="comandos-asociaciones.cancelar_asociacion",
            schema=AvroSchema(ComandoCancelarAsociacionEstrategica),
        )        