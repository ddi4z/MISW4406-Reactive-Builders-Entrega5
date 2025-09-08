from dataclasses import dataclass, field
from alpespartners.seedwork.aplicacion.dto import DTO


@dataclass(frozen=True)
class ReservaDTO(DTO):
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    id: str = field(default_factory=str)
    

@dataclass(frozen=True)
class PlataformaDTO(DTO):
    nombre: str = field(default_factory=str)
    

@dataclass(frozen=True)
class MedioMarketingDTO(DTO):
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    id: str = field(default_factory=str)
    plataforma: PlataformaDTO = field(default_factory=PlataformaDTO)
    
    



@dataclass(frozen=True)
class PublicacionDTO(DTO):
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    id: str = field(default_factory=str)
    
@dataclass(frozen=True)
class EventoDTO(DTO):
    id: str = field(default_factory=str)
    tipo_evento: str = field(default_factory=str)
    fecha_evento: str = field(default_factory=str)