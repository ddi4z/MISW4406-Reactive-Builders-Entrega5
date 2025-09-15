import os
import requests
import strawberry
from typing import Optional, List

ASSOCIATIONS_HOST = os.getenv("ASSOCIATIONS_HOST", "localhost")
ASSOCIATIONS_PORT = int(os.getenv("ASSOCIATIONS_PORT", "5000"))
BASE_URL = f"http://{ASSOCIATIONS_HOST}:{ASSOCIATIONS_PORT}"

# ===== Tipos GraphQL =====

@strawberry.type
class Vigencia:
    fechaInicio: Optional[str]
    fechaFin: Optional[str]

@strawberry.type
class Asociacion:
    id: str
    idMarca: str
    idSocio: str
    tipo: Optional[str]
    descripcion: Optional[str]
    vigencia: Optional[Vigencia]
    estado: Optional[str]
    fechaCreacion: Optional[str]
    fechaActualizacion: Optional[str]

@strawberry.input
class VigenciaInput:
    fecha_inicio: str
    fecha_fin: str

@strawberry.input
class CrearAsociacionInput:
    id_marca: str
    id_socio: str
    tipo: str
    descripcion: Optional[str] = None
    vigencia: Optional[VigenciaInput] = None

@strawberry.type
class Respuesta:
    mensaje: str
    codigo: int
    idSolicitud: Optional[str] = None

# ===== Helpers REST =====

def _get(path: str):
    r = requests.get(f"{BASE_URL}{path}", timeout=10)
    r.raise_for_status()
    return r.json()

def _post(path: str, json: dict):
    r = requests.post(f"{BASE_URL}{path}", json=json, timeout=15)
    r.raise_for_status()
    body = r.json() if r.content and r.headers.get("content-type","").startswith("application/json") else {}
    return {"status_code": r.status_code, "body": body}

# ===== Mapper =====

def map_asociacion(dto: dict) -> Asociacion:
    vig = dto.get("vigencia") or {}
    return Asociacion(
        id=str(dto.get("id")),
        idMarca=str(dto.get("id_marca")),
        idSocio=str(dto.get("id_socio")),
        tipo=dto.get("tipo"),
        descripcion=dto.get("descripcion"),
        vigencia=Vigencia(
            fechaInicio=vig.get("fecha_inicio"),
            fechaFin=vig.get("fecha_fin"),
        ) if vig else None,
        estado=dto.get("estado"),
        fechaCreacion=dto.get("fecha_creacion"),
        fechaActualizacion=dto.get("fecha_actualizacion"),
    )

# ===== Llamadas usadas por Query/Mutation =====
'''
def obtener_asociaciones() -> List[Asociacion]:
    data = _get("/asociaciones")
    if isinstance(data, dict) and "items" in data:
        data = data["items"]
    return [map_asociacion(x) for x in data]
'''
def obtener_asociaciones_por_marca(id_marca: str) -> List[Asociacion]:
    data = _get(f"/asociaciones/marca/{id_marca}")
    return [map_asociacion(x) for x in data]
'''
def obtener_asociacion(id_asociacion: str) -> Asociacion:
    data = _get(f"/asociaciones/{id_asociacion}")
    return map_asociacion(data)
'''
def crear_asociacion(payload: dict) -> Respuesta:
    resp = _post("/asociaciones", json=payload)
    body = resp["body"] or {}
    return Respuesta(
        mensaje=body.get("mensaje", "Procesando"),
        codigo=resp["status_code"],  # 202 si es async
        idSolicitud=body.get("id_correlacion") or body.get("idSolicitud")
    )
