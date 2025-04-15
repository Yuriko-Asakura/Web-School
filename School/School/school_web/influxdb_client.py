from influxdb_client import InfluxDBClient
from django.conf import settings

def get_influxdb_client():
    return InfluxDBClient(
        url=settings.INFLUXDB_SETTINGS['http://localhost:8086'],
        token=settings.INFLUXDB_SETTINGS['AN0s_moZ0YLY_zP6RTlzTQiFqkDwfiNsWu-D_O-OmBETCBMqBJrB59kTxygPlZOs32HuIgrkKJQaV_Lt_mm5Og=='],
        org=settings.INFLUXDB_SETTINGS['MPT']
    )
    
