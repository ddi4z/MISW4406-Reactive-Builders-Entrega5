FROM python:3.12-slim

WORKDIR /app

COPY pagos-requirements.txt .
RUN pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel \
    && pip install --no-cache-dir -r pagos-requirements.txt \
    && pip install --no-cache-dir uvicorn gunicorn


COPY . /app

ENV PYTHONPATH=/app/src

ENV PORT=8080

# Exponemos el puerto
EXPOSE 8080

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "--bind", "0.0.0.0:8080", "pagos.api.pagos:app"]
