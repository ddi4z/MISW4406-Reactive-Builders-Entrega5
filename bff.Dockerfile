FROM python:3.12-slim
WORKDIR /app
COPY bff-requirements.txt .
RUN pip install --no-cache-dir -r bff-requirements.txt
COPY src/bff_web ./src/bff_web
ENV PYTHONPATH=/app/src
EXPOSE 8003
CMD ["uvicorn", "bff_web.main:app", "--host", "0.0.0.0", "--port", "8003"]
