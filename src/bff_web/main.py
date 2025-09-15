from fastapi import FastAPI
from .api.v1.router import router as v1


app = FastAPI(title="Reactive Builders BFF")
app.include_router(v1, prefix="/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
