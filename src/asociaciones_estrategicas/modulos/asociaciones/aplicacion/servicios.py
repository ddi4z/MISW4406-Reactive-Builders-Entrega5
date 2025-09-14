from asociaciones_estrategicas.modulos.asociaciones.infraestructura.schema.v1.comandos import (
    ComandoIniciarTracking, ComandoIniciarTrackingPayload
)
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.despachadores import Despachador

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
