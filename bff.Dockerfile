FROM python:3.11-slim

WORKDIR /app

# Copiar solo el código del BFF
COPY ./src/bff_web /app/bff_web

# Instalar dependencias del BFF
RUN pip install --no-cache-dir -r /app/bff_web/bff-requirements.txt \
    && pip install --no-cache-dir uvicorn

# Variables de entorno
ENV PYTHONPATH=/app
ENV PORT=8080

# Ejecutar FastAPI con Uvicorn en el puerto 8080 (requerido por Cloud Run)
CMD ["uvicorn", "bff_web.main:app", "--host", "0.0.0.0", "--port", "8080"]
