from datetime import datetime
import pulsar, _pulsar
from pulsar.schema import AvroSchema
import logging
import traceback

from pagos.modulos.pagos.aplicacion.comandos.realizar_pago_comision import RealizarPagoComision
from pagos.modulos.pagos.infraestructura.schema.v1.comandos import (
    ComandoRealizarPagoComision,
    ComandoRevertirPagoComision,
)

""" from pagos.modulos.asociaciones.infraestructura.proyecciones import (
    ProyeccionAsociacionesTotales,
    ProyeccionAsociacionesLista,
) """
from pagos.seedwork.aplicacion.comandos import ejecutar_commando
from pagos.seedwork.infraestructura import utils
from pagos.modulos.pagos.aplicacion.comandos.revertir_pago_comision import RevertirPagoComision


def suscribirse_a_eventos(app=None):
    ...

""" 
def suscribirse_a_eventos(app=None):
    pass
    cliente = None
    try:
        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        consumidor = cliente.subscribe(
            "eventos-asociacion",
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name="alpes-partners-sub-eventos",
            schema=AvroSchema(EventoEvento),
        )

        while True:
            mensaje = consumidor.receive()
            try:
                datos = mensaje.value().data
                mensaje_evento = mensaje.value()
                print(f"Evento recibido:{mensaje_evento.estado} {datos}")
                logging.info(f"Evento recibido:{mensaje_evento.estado} {datos}")

                if mensaje_evento.estado == "OnboardingIniciado":
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

                elif mensaje_evento.estado == "OnboardingCancelado":
                    with app.app_context():
                        asociacion = AsociacionEstrategica.query.filter_by(id=datos.id_asociacion).first()
                        if asociacion:
                            ejecutar_proyeccion(
                                ProyeccionAsociacionesTotales(
                                    asociacion.fecha_creacion,
                                    asociacion.tipo,
                                    ProyeccionAsociacionesTotales.DELETE
                                ),
                                app=app,
                            )
                            ejecutar_proyeccion(
                                ProyeccionAsociacionesLista(
                                    datos.id_asociacion,
                                    operacion=ProyeccionAsociacionesLista.DELETE
                                ),
                                app=app,
                            )                            
                        else:
                            logging.warning(f"No se encontró asociación con id {datos.id_asociacion} para cancelar")
                                                    

                elif mensaje_evento.estado == "OnboardingFallido":
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
 """
def suscribirse_a_comandos_crear(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        consumidor = cliente.subscribe(
            "comandos-pagos.realizar_pago_comision",
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name="eventos-sub-comandos-crear",
            schema=AvroSchema(ComandoRealizarPagoComision),
        )

        while True:
            mensaje = consumidor.receive()
            comando_integracion = mensaje.value()
            datos = comando_integracion.data
  
            logging.info(f"Comando recibido RealizarPagoComision: {datos}")
            print(f"Comando recibido RealizarPagoComision: {datos}")





            comando = RealizarPagoComision(
                id_correlacion = datos.id_correlacion,
                id = '',
                fecha_creacion = '' ,
                fecha_actualizacion = '',
                id_comision = datos.id_comision,
                moneda = datos.moneda,
                monto= datos.monto,
                metodo_pago= datos.metodo_pago,
                estado= datos.estado,
                pasarela= datos.pasarela,
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


def suscribirse_a_comandos_revertir(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        consumidor = cliente.subscribe(
            "comandos-pagos.revertir_pago_comision",
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name="eventos-sub-comandos-revertir",
            schema=AvroSchema(ComandoRevertirPagoComision),
        )

        while True:
            mensaje = consumidor.receive()
            comando_integracion = mensaje.value()
            datos = comando_integracion.data

    
            logging.info(f"Comando recibido RevertirPago: {datos}")
            print(f"Comando recibido Revertir: {datos}")

            comando = RevertirPagoComision(
                id_correlacion= datos.id_correlacion,
                id_pago = datos.id_pago,
                fecha_creacion = '',
                fecha_actualizacion = '',
                motivo= datos.motivo
            )

            # Captura errores por cada mensaje
            try:
                with app.app_context():
                    ejecutar_commando(comando)

                consumidor.acknowledge(mensaje)

            except Exception as e:
                logging.error(f"Error procesando comando Revertir: {e}")
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
