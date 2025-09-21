from eventos_y_atribucion.modulos.eventos_medios.infraestructura.mapeadores import MapeadorEventosEvento
import pulsar
from pulsar.schema import AvroSchema

from eventos_y_atribucion.seedwork.infraestructura import utils
from .schema.v1.eventos import EventoEvento  

class Despachador:
    def __init__(self):
        self.mapper = MapeadorEventosEvento()

    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        #cliente.close()

    def publicar_evento(self, evento, topico):
        evento_integracion = self.mapper.entidad_a_dto(evento)
        # forzamos el AvroSchema del evento unificado
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoEvento))

    def publicar_comando(self, comando, topico, schema=None):
        # Si el comando ya es un Avro Record con schema conocido
        schema = schema or AvroSchema(comando.__class__)
        self._publicar_mensaje(comando, topico, schema)