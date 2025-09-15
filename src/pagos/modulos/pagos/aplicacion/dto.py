from abc import ABC
from dataclasses import dataclass, field
from eventos_y_atribucion.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class ComisionDTO(DTO):
    id: str = field(default_factory=str)
    valor: int = field(default_factory=int)
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    id_evento: str = field(default_factory=str)
    
@dataclass(frozen=True)
class RecompensaDTO(DTO):
    id: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    id_evento: str = field(default_factory=str)