from dataclasses import dataclass
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.despachadores import Despachador
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.schema.v1.comandos import ComandoIniciarTracking, ComandoIniciarTrackingPayload
from asociaciones_estrategicas.seedwork.aplicacion.comandos import Comando
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.dto import AsociacionDTO, VigenciaDTO
from .base import CrearAsociacionBaseHandler
from asociaciones_estrategicas.seedwork.aplicacion.comandos import ejecutar_commando as comando

from asociaciones_estrategicas.modulos.asociaciones.dominio.entidades import AsociacionEstrategica
from asociaciones_estrategicas.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.mapeadores import MapeadorAsociacion
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.repositorios import (
    RepositorioAsociacionEstrategica,
    RepositorioEventosAsociacionEstrategica,
)
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.servicios import ServicioTracking

# ==========
# Comando
# ==========

@dataclass
class CrearAsociacion(Comando):
    id: str
    id_correlacion: str
    id_marca: str
    id_socio: str
    tipo: str
    descripcion: str
    fecha_inicio: str
    fecha_fin: str
    fecha_creacion: str = ""
    fecha_actualizacion: str = ""


# ==========
# Handler
# ==========

class CrearAsociacionHandler(CrearAsociacionBaseHandler):

    def handle(self, comando: CrearAsociacion):
        # 1. Crear el DTO desde el comando
        asociacion_dto = AsociacionDTO(
            id=comando.id,
            id_marca=comando.id_marca,
            id_socio=comando.id_socio,
            tipo=comando.tipo,
            descripcion=comando.descripcion,
            vigencia=VigenciaDTO(
                fecha_inicio=comando.fecha_inicio,
                fecha_fin=comando.fecha_fin,
            ),
            fecha_creacion=comando.fecha_creacion,
            fecha_actualizacion=comando.fecha_actualizacion,
        )

        # 2. Convertir a entidad de dominio
        asociacion: AsociacionEstrategica = self.fabrica_asociaciones.crear_objeto(
            asociacion_dto, MapeadorAsociacion()
        )

        # 3. Ejecutar lógica de creación con id_correlacion de la saga
        asociacion.crear_asociacion(asociacion, in_id_correlacion=comando.id_correlacion)

        # 4. Persistir asociación + eventos
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioAsociacionEstrategica)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosAsociacionEstrategica)

        UnidadTrabajoPuerto.registrar_batch(
            repositorio.agregar,
            asociacion,
            repositorio_eventos_func=repositorio_eventos.agregar,
        )
        UnidadTrabajoPuerto.commit()

        # 5. Disparar Tracking (parte de la saga en paso 2)
        # Será responsabilidad de la saga en orquestación
        ##ServicioTracking().iniciar_tracking(asociacion)


# ==========
# Registro
# ==========

@comando.register(CrearAsociacion)
def ejecutar_comando_crear_asociacion(comando: CrearAsociacion):
    handler = CrearAsociacionHandler()
    handler.handle(comando)
