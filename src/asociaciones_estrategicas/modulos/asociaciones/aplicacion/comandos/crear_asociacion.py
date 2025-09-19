from dataclasses import dataclass
import logging
from asociaciones_estrategicas.modulos.asociaciones.dominio.eventos import OnboardingFallido
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.despachadores import Despachador
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.schema.v1.comandos import ComandoIniciarTracking, ComandoIniciarTrackingPayload
from asociaciones_estrategicas.seedwork.aplicacion.comandos import Comando
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.dto import AsociacionDTO, VigenciaDTO
from asociaciones_estrategicas.seedwork.dominio.excepciones import ReglaNegocioExcepcion
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

    def handle(self, comando):
        try:
            # 1. Construir DTO desde el comando
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

            # 2. Usar la fábrica (valida reglas de negocio)
            asociacion: AsociacionEstrategica = self.fabrica_asociaciones.crear_objeto(
                asociacion_dto, MapeadorAsociacion()
            )

            # 3. Ejecutar la creación en la entidad → emite OnboardingIniciado
            asociacion.crear_asociacion(asociacion, in_id_correlacion=comando.id_correlacion)

            # 4. Guardar entidad + eventos
            repositorio = self.fabrica_repositorio.crear_objeto(RepositorioAsociacionEstrategica)
            repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosAsociacionEstrategica)

            UnidadTrabajoPuerto.registrar_batch(
                repositorio.agregar,
                asociacion,
                repositorio_eventos_func=repositorio_eventos.agregar,
            )
            UnidadTrabajoPuerto.commit()

        except ReglaNegocioExcepcion as e:
            print(f"Procesando la exepcion dentro del handler {e}")
            logging.warning(f"[SAGA] OnboardingFallido emitido: {str(e)} (id_correlacion={comando.id_correlacion})")

            # Caso: la regla falló en la fábrica
            asociacion = AsociacionEstrategica()
            asociacion.agregar_evento(OnboardingFallido(
                id_correlacion=comando.id_correlacion,
                id_asociacion=comando.id,   # id del comando
                motivo=str(e),
            ))

            repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosAsociacionEstrategica)

            UnidadTrabajoPuerto.registrar_batch(
                lambda x: None,   # no persistimos la entidad
                asociacion,
                repositorio_eventos_func=repositorio_eventos.agregar,
            )
            UnidadTrabajoPuerto.commit()
  

# ==========
# Registro
# ==========

@comando.register(CrearAsociacion)
def ejecutar_comando_crear_asociacion(comando: CrearAsociacion):
    handler = CrearAsociacionHandler()
    handler.handle(comando)
