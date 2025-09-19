import pulsar, _pulsar
from pulsar.schema import AvroSchema
import logging
import traceback

from asociaciones_estrategicas.config.uow import UnidadTrabajoPulsar
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.comandos.crear_asociacion import CrearAsociacion, CrearAsociacionHandler
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.schema.v1.comandos import ComandoCrearAsociacionEstrategica
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.schema.v1.eventos import (
    EventoOnboardingIniciado,
)
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.proyecciones import (
    ProyeccionAsociacionesTotales,
    ProyeccionAsociacionesLista,
)
from asociaciones_estrategicas.seedwork.aplicacion.comandos import ejecutar_commando
from asociaciones_estrategicas.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from asociaciones_estrategicas.seedwork.infraestructura import utils
from asociaciones_estrategicas.seedwork.infraestructura.uow import guardar_unidad_trabajo
from asociaciones_estrategicas.config.uow import UnidadTrabajoHibrida


def suscribirse_a_eventos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        consumidor = cliente.subscribe(
            "eventos-asociacion",
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name="alpes-partners-sub-eventos",
            schema=AvroSchema(EventoOnboardingIniciado),
        )

        while True:
            mensaje = consumidor.receive()
            try:
                datos = mensaje.value().data
                mensaje_evento = mensaje.value()
                print(f"Evento recibido:{mensaje_evento.type} {datos}")
                logging.info(f"Evento recibido:{mensaje_evento.type} {datos}")

                if mensaje_evento.type == "OnboardingIniciado":
                    ejecutar_proyeccion(
                        ProyeccionAsociacionesTotales(
                            datos.fecha_creacion,
                            datos.tipo,
                            ProyeccionAsociacionesTotales.ADD
                        ),
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
                            datos.fecha_creacion,
                        ),
                        app=app,
                    )

                elif mensaje_evento.type == "AsociacionFinalizada":
                    # TODO: implementar actualización de proyecciones si aplica
                    pass

                else:
                    logging.warning(f"Evento desconocido: {mensaje_evento.type}")

                consumidor.acknowledge(mensaje)

            except Exception as e:
                logging.error(f"Error procesando evento de asociación: {e}")
                traceback.print_exc()
                # ⚖️ decisión: descartar (ack) o reintentar (nack)
                consumidor.acknowledge(mensaje)
                # consumidor.negative_acknowledge(mensaje)

        cliente.close()
    except Exception:
        logging.error("ERROR: Suscribiéndose al tópico de eventos!")
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        consumidor = cliente.subscribe(
            "comandos-asociaciones.crear_asociacion",
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name="asociaciones-sub-comandos",
            schema=AvroSchema(ComandoCrearAsociacionEstrategica),
        )

        while True:
            mensaje = consumidor.receive()
            comando_integracion = mensaje.value()
            datos = comando_integracion.data

    
            logging.info(f"Comando recibido CrearAsociacion: {datos}")
            print(f"Comando recibido CrearAsociacion: {datos}")

            comando = CrearAsociacion(
                id="",
                id_correlacion=datos.id_correlacion,
                id_marca=datos.id_marca,
                id_socio=datos.id_socio,
                tipo=datos.tipo,
                descripcion=datos.descripcion,
                fecha_inicio=datos.fecha_inicio,
                fecha_fin=datos.fecha_fin,
                fecha_creacion="",
                fecha_actualizacion="",
            )

            # Captura errores por cada mensaje
            try:
                with app.app_context():
                    ejecutar_commando(comando)

                consumidor.acknowledge(mensaje)

            except Exception as e:
                logging.error(f"Error procesando comando CrearAsociacion: {e}")
                traceback.print_exc()

                # decisión: descartar o reintentar
                consumidor.acknowledge(mensaje)   # descartar (ej: error de negocio)
                # consumidor.negative_acknowledge(mensaje)  # reintentar (ej: error técnico)

        cliente.close()

    except Exception:
        logging.error("ERROR: Suscribiéndose al tópico de comandos!")
        traceback.print_exc()
        if cliente:
            cliente.close()
