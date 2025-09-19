import pulsar
from pulsar.schema import AvroSchema

from asociaciones_estrategicas.seedwork.infraestructura import utils
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.mapeadores import MapeadorEventosAsociacionEstrategica


class Despachador:
    def __init__(self):
        self.mapper = MapeadorEventosAsociacionEstrategica()

    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # Convertir evento de dominio a evento de integración
        evento_integracion = self.mapper.entidad_a_dto(evento)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(evento_integracion.__class__))

    def publicar_comando(self, comando, topico, schema=None):
        # Si el comando ya es un Avro Record con schema conocido
        schema = schema or AvroSchema(comando.__class__)
        self._publicar_mensaje(comando, topico, schema)