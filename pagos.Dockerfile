FROM python:3.12-slim


WORKDIR /app


COPY pagos-requirements.txt .
RUN pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel
RUN pip install --no-cache-dir -r pagos-requirements.txt

COPY . .


WORKDIR /app/src


EXPOSE 8001

CMD ["python", "-m", "uvicorn", "pagos.api.pagos:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]

