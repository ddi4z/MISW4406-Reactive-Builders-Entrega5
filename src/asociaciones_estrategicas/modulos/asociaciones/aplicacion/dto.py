from dataclasses import dataclass, field
from asociaciones_estrategicas.seedwork.aplicacion.dto import DTO


@dataclass(frozen=True)
class VigenciaDTO(DTO):
    fecha_inicio: str
    fecha_fin: str

@dataclass(frozen=True)
class AsociacionDTO(DTO):
    id: str = field(default_factory=str)
    id_marca: str = field(default_factory=str)
    id_socio: str = field(default_factory=str)
    tipo: str = field(default_factory=str)          # Enum serializado como string
    descripcion: str = field(default_factory=str)
    vigencia: VigenciaDTO = None
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
