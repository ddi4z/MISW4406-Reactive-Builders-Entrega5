import time
import os
import datetime

epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)

def time_millis():
    return int(time.time() * 1000)

def unix_time_millis(dt):
    # Aseguramos que dt tenga tzinfo UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return (dt - epoch).total_seconds() * 1000.0

def millis_a_datetime(millis):
    return datetime.datetime.fromtimestamp(millis/1000.0)

def broker_host():
    return os.getenv('BROKER_HOST', default="localhost")

