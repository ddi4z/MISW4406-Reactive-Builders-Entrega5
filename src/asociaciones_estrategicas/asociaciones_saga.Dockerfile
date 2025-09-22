FROM python:3.11-slim

WORKDIR /app

# copiamos todo el contenido de asociaciones_estrategicas
#COPY . /app/asociaciones_estrategicas
#COPY ../../src/eventos_y_atribucion /app/eventos_y_atribucion
#COPY ../../src/pagos /app/pagos
#COPY src/ /app
COPY ./src/eventos_y_atribucion /app/eventos_y_atribucion
COPY ./src/pagos /app/pagos
COPY ./src/asociaciones_estrategicas /app/asociaciones_estrategicas

# instalamos dependencias
RUN pip install --no-cache-dir -r /app/asociaciones_estrategicas/asociaciones-requirements.txt \
    && pip install gunicorn

# añadimos src al PYTHONPATH
ENV PYTHONPATH=/app

# Variable de entorno para Cloud Run
ENV PORT=8080


# arrancamos con Gunicorn apuntando al factory de Flask
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8080", "asociaciones_estrategicas.api:create_app()"
