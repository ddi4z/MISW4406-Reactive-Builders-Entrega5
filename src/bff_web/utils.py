import time
import os
import datetime
import requests
import json
from fastavro.schema import parse_schema
from pulsar.schema import *

epoch = datetime.datetime.utcfromtimestamp(0)
PULSAR_ENV: str = 'BROKER_HOST'

def time_millis():
    return int(time.time() * 1000)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

def millis_a_datetime(millis):
    return datetime.datetime.fromtimestamp(millis/1000.0)

def broker_host():
    return os.getenv(PULSAR_ENV, default="localhost")

def consultar_schema_registry(topico: str) -> dict:
    resp = requests.get(
        f'http://{broker_host()}:8080/admin/v2/schemas/{topico}/schema'
    )
    json_registry = resp.json()  # dict
    data = json_registry.get("data", {})

    # Si 'data' ya es un dict lo devolvemos tal cual, si es str lo convertimos
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            # el string no es un JSON válido, devolvemos vacío o lo que necesites
            return {}
    return data

def obtener_schema_avro_de_diccionario(json_schema: dict) -> AvroSchema:
    definicion_schema = parse_schema(json_schema)
    return AvroSchema(None, schema_definition=definicion_schema)

