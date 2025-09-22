FROM python:3.11-slim

WORKDIR /app


COPY src/ /app


COPY pagos-requirements.txt /app/


RUN pip install --no-cache-dir -r /app/pagos-requirements.txt \
    && pip install --no-cache-dir gunicorn

ENV PYTHONPATH=/app
ENV PORT=5003


CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5003", "pagos.api:app"]
