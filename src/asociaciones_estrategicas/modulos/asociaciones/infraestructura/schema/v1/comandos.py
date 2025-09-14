from pulsar.schema import *
from dataclasses import dataclass, field
from asociaciones_estrategicas.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearAsociacionEstrategicaPayload(ComandoIntegracion):
    id_usuario = String()
    id_marca = String()
    id_socio = String()
    tipo = String()
    descripcion = String()
    # TODO vigencia: PeriodoVigencia = None    
    # TODO Cree los records para itinerarios

class ComandoCrearAsociacionEstrategica(ComandoIntegracion):
    data = ComandoCrearAsociacionEstrategicaPayload()


# Payload: solo los datos de negocio
class ComandoIniciarTrackingPayload(Record):
    id_asociacion_estrategica = String()
    id_marca = String()
    id_socio = String()
    tipo = String()

# Comando: metadatos + payload
class ComandoIniciarTracking(ComandoIntegracion):
    data = ComandoIniciarTrackingPayload()    