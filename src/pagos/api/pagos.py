from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text

import asyncio
from contextlib import asynccontextmanager

from pagos.modulos.pagos.aplicacion.comandos.crear_pago import CrearPago
from pagos.modulos.pagos.aplicacion.comandos.revertir_pago import RevertirPago
from pagos.modulos.pagos.aplicacion.mapeadores import MapeadorPagoDTOJson
from pagos.seedwork.aplicacion.comandos import ejecutar_commando
from pagos.seedwork.dominio.excepciones import ExcepcionDominio
from pydantic_settings import BaseSettings
from typing import Any


from ..config.db import Base, engine
from ..config.db_dependencies import get_db


class Config(BaseSettings):
    APP_VERSION: str = "1"

settings = Config()
app_configs: dict[str, Any] = {"title": "Pagos AeroAlpes"}
tasks = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    # task1 = asyncio.create_task(suscribirse_a_topico("evento-pago", "sub-pagos", EventoPago))
    # task2 = asyncio.create_task(suscribirse_a_topico("comando-pagar-reserva", "sub-com-pagos-reservar", ComandoPagarReserva))
    # task3 = asyncio.create_task(suscribirse_a_topico("comando-revertir-pago", "sub-com-pagos-revertir", ComandoRevertirPago))
    # tasks.extend([task1, task2, task3])

    yield

    # for task in tasks:
        # task.cancel()
    
app = FastAPI(lifespan=lifespan, **app_configs)



@app.get("/pagos/ping")
def ping(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar()
    return {"pong": result}




    
@app.post("/pagos", include_in_schema=False)
async def prueba_pagar_reserva(request: Request) -> dict[str, str]:
    try:
        pago_dict = await request.json()

        map_evento = MapeadorPagoDTOJson()
        pago_dto = map_evento.externo_a_dto(pago_dict)

        comando = CrearPago(            
            pago_dto.id,
            pago_dto.fecha_creacion,
            pago_dto.fecha_actualizacion,
            pago_dto.id_correlacion,
            pago_dto.id_comision,
            pago_dto.moneda,
            pago_dto.monto,
            pago_dto.metodo_pago,
            pago_dto.estado,
            pago_dto.pasarela
        )

        ejecutar_commando(comando)
        
        return {"status": "accepted"}
    except ExcepcionDominio as e:
        return {"error": str(e)}

@app.post("/pagos/revertir", include_in_schema=False)
async def prueba_revertir_pago(request: Request) -> dict[str, str]:
    try:
        pago_dict = await request.json()

        map_evento = MapeadorPagoDTOJson()
        pago_dto = map_evento.externo_a_dto(pago_dict)


        comando = RevertirPago(pago_dto.id)

        ejecutar_commando(comando)
        
        return {"status": "accepted"} 
    except ExcepcionDominio as e:
        return {"error": str(e)}