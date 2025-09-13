import pulsar, _pulsar
from pulsar.schema import AvroSchema
import logging
import traceback

from asociaciones_estrategicas.modulos.asociaciones.infraestructura.schema.v1.eventos import (
    EventoAsociacionCreada,
    EventoAsociacionFinalizada,
)
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.proyecciones import (
    ProyeccionAsociacionesTotales,
    ProyeccionAsociacionesLista,
)
from asociaciones_estrategicas.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from asociaciones_estrategicas.seedwork.infraestructura import utils


def suscribirse_a_eventos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        consumidor = cliente.subscribe(
            "eventos-asociacion",
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name="alpes-partners-sub-eventos",
            schema=AvroSchema(EventoAsociacionCreada),
        )

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            mensaje_evento = mensaje.value()   # Evento completo
            print(f"Evento recibido: {datos}")

            # TODO: distinguir si el evento es creación, actualización o eliminación
            if mensaje_evento.type == "AsociacionCreada":
                ejecutar_proyeccion(
                    ProyeccionAsociacionesTotales(datos.fecha_creacion, ProyeccionAsociacionesTotales.ADD),
                    app=app,
                )

                ejecutar_proyeccion(
                    ProyeccionAsociacionesLista(
                        datos.id_asociacion,
                        datos.id_marca,
                        datos.id_socio,
                        datos.tipo,
                        datos.descripcion,           
                        datos.fecha_inicio,          
                        datos.fecha_fin,             
                        datos.fecha_creacion,
                        datos.fecha_creacion,        # fecha_actualizacion inicial
                    ),
                    app=app,
                )

            elif mensaje_evento.type == "AsociacionFinalizada":
                pass # TODO: implementar si se requiere actualizar alguna proyección existente o crear
                # quizás otra proyección específica
            else:
                logging.warning(f"Evento desconocido: {mensaje_evento.type}")




            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error("ERROR: Suscribiéndose al tópico de eventos!")
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        # TODO: definir schema de comandos de asociación si se requiere
        logging.info("Suscripción a comandos no implementada todavía")
    except:
        logging.error("ERROR: Suscribiéndose al tópico de comandos!")
        traceback.print_exc()
        if cliente:
            cliente.close()
