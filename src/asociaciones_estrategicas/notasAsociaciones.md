
Formas de levantar:
1. DOCKER-COMPOSE: Por ahora no funciona
Levantar por docker-compose micro asociaciones 
docker compose --profile asociaciones_estrategicas --profile pulsar up --force-recreate --build


2. Applicaciones individuales
Base de datos asociaciones
docker-compose --profile db_asociaciones_estrategicas up

Broker
docker-compose --profile pulsar up

Subir la app
flask --app src/asociaciones_estrategicas/api --debug run --host=0.0.0.0 --port=5000




NOTA:
Una cosa que no menciono en el video es que como se usa Event Sourcing 
en el docker-compose deje un nuevo componente que fija la retención en -1 de los topicos para que persistan
./bin/pulsar-admin namespaces set-retention public/default --size -1 --time -1


class TipoAsociacion(Enum):
    PROGRAMA_AFILIADOS = "programa_afiliados"
    COLABORACION_DIRECTA = "colaboracion_directa"
    CAMPANIA = "campania"
    PROGRAMA_LEALTAD = "programa_lealtad"
    ALIANZA_B2B = "alianza_b2b"
    
	
Base de datos asociaciones
docker-compose --profile db_asociaciones_estrategicas up

Broker
docker-compose --profile pulsar up

Subir la app
flask --app src/asociaciones_estrategicas/api --debug run --host=0.0.0.0 --port=5000



Escuchar los topicos

docker exec -it broker bash
./bin/pulsar-client consume -s "sub-datos" public/default/eventos-asociacion -n 0 


docker exec -it broker bash
./bin/pulsar-client consume -s "sub-datos" comandos-eventos_y_atribucion.iniciar_tracking -n 0



from pulsar.schema import *
from asociaciones_estrategicas.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from asociaciones_estrategicas.seedwork.infraestructura.utils import time_millis
import uuid


# ======================
# Payloads
# ======================

class AsociacionCreadaPayload(Record):
    id_asociacion = String()
    id_marca = String()
    id_socio = String()
    tipo = String()
    descripcion = String()      
    fecha_inicio = Long()       
    fecha_fin = Long()          
    fecha_creacion = Long()



class AsociacionFinalizadaPayload(Record):
    id_asociacion = String()
    fecha_actualizacion = Long()


# ======================
# Eventos de integración
# ======================

# ======================
# Payloads
# ======================

TOPICO: public/default/eventos-asociacion 

class AsociacionCreadaPayload(Record):
    id_asociacion = String()
    id_marca = String()
    id_socio = String()
    tipo = String()
    descripcion = String()      
    fecha_inicio = Long()       
    fecha_fin = Long()          
    fecha_creacion = Long()


class EventoAsociacionCreada(EventoIntegracion):
    # NOTE La librería Record de Pulsar no es capaz de reconocer campos heredados, 
    # por lo que los mensajes al ser codificados pierden sus valores
    # Dupliqué el los cambios que ya se encuentran en la clase Mensaje
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = AsociacionCreadaPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


TOPICO comandos-eventos_y_atribucion.iniciar_tracking

# Payload: solo los datos de negocio
class ComandoIniciarTrackingPayload(Record):
    id_asociacion_estrategica = String()
    id_marca = String()
    id_socio = String()
    tipo = String()

# Comando: metadatos + payload
class ComandoIniciarTracking(ComandoIntegracion):
    data = ComandoIniciarTrackingPayload()    
	
	
	
# Comando: Crear Asociacion estrategica
TOPICO 	comandos-asociaciones.crear_asociacion
class ComandoCrearAsociacionEstrategicaPayload(ComandoIntegracion):
    id_usuario = String()
    id_marca = String()
    id_socio = String()
    tipo = String()
    descripcion = String()
    fecha_inicio = String()
    fecha_fin = String()


class ComandoCrearAsociacionEstrategica(ComandoIntegracion):
    data = ComandoCrearAsociacionEstrategicaPayload()


