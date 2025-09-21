from fastapi import FastAPI
import asyncio
from contextlib import asynccontextmanager

from .consumidores import suscribirse_a_topico
from .api.v1.router import router as v1

tasks = []
eventos = list()

@asynccontextmanager
async def lifespan(app: FastAPI):
    task1 = asyncio.ensure_future(suscribirse_a_topico("eventos-asociacion-estrategica", "alpespartners-bff", "public/default/eventos-asociacion-estrategica", eventos=eventos))
    tasks.append(task1)

    yield

    for task in tasks:
        task.cancel()

app = FastAPI(lifespan=lifespan, title="Reactive Builders BFF")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(v1, prefix="/v1")
