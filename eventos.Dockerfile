FROM python:3.11-slim

WORKDIR /app


COPY . /app/eventos_y_atribucion


RUN pip install --no-cache-dir -r /app/eventos_y_atribucion/eventos-requirements.txt \
    && pip install --no-cache-dir gunicorn


ENV PYTHONPATH=/app


ENV PORT=8080

CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8080", "eventos_y_atribucion.api:create_app()"]
