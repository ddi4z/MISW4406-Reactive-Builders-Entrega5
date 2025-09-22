import pulsar
from pulsar.schema import *

from pagos.modulos.pagos.infraestructura.mapeadores import MapeadorEventosPago
from pagos.modulos.pagos.infraestructura.schema.v1.eventos import EventoPago
from . import utils


class Despachador:
    def __init__(self):
        self.mapper = MapeadorEventosPago()

    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        #cliente.close()

    def publicar_evento(self, evento, topico):
        evento_integracion = self.mapper.entidad_a_dto(evento)
        # forzamos el AvroSchema del evento unificado
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoPago))

    def publicar_comando(self, comando, topico, schema=None):
        # Si el comando ya es un Avro Record con schema conocido
        schema = schema or AvroSchema(comando.__class__)
        self._publicar_mensaje(comando, topico, schema)