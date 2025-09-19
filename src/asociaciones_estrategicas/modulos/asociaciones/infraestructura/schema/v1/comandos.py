from pulsar.schema import *
from dataclasses import dataclass, field
from asociaciones_estrategicas.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from pulsar.schema import AvroSchema

class ComandoCrearAsociacionEstrategicaPayload(ComandoIntegracion):
    id_correlacion = String()
    id_usuario = String()
    id_marca = String()
    id_socio = String()
    tipo = String()
    descripcion = String()
    fecha_inicio = String()
    fecha_fin = String()


class ComandoCrearAsociacionEstrategica(ComandoIntegracion):
    data = ComandoCrearAsociacionEstrategicaPayload()


# Payload: solo los datos de negocio
class ComandoIniciarTrackingPayload(ComandoIntegracion):
    id_asociacion_estrategica = String()
    id_marca = String()
    id_socio = String()
    tipo = String()

# Comando: metadatos + payload
class ComandoIniciarTracking(ComandoIntegracion):
    data = ComandoIniciarTrackingPayload()    

class RevertirAsociacionPayload(ComandoIntegracion):
    id_correlacion = String()
    id_asociacion = String()
    motivo = String()

class ComandoRevertirAsociacion(ComandoIntegracion):
    data = RevertirAsociacionPayload()