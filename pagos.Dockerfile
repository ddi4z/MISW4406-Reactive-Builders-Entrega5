FROM python:3.11-slim

WORKDIR /app


COPY ./src/pagos /app/pagos



RUN pip install --no-cache-dir -r /app/pagos/pagos-requirements.txt \
    && pip install --no-cache-dir gunicorn


ENV PYTHONPATH=/app


ENV PORT=8080

CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8080", "pagos.api:create_app()"]
