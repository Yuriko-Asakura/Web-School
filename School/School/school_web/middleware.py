import os
import time
import psutil
from prometheus_client import Counter, Gauge, Histogram, start_http_server
from django.utils.deprecation import MiddlewareMixin

# Инициализация метрик
class DjangoMetrics:
    def __init__(self):
        # Системные метрики
        self.SYSTEM_CPU = Gauge(
            'django_system_cpu_percent', 
            'System-wide CPU usage percent'
        )
        self.PROCESS_CPU = Gauge(
            'django_process_cpu_percent',
            'Current CPU usage by Django process (%)'
        )
        self.LOAD_AVG = Gauge(
            'django_system_load_avg',
            'System load average',
            ['period']  # 1min, 5min, 15min
        )
        self.RAM_USAGE = Gauge(
            'django_system_ram_usage',
            'System RAM usage percent'
        )
        
        # Метрики запросов
        self.REQUEST_COUNT = Counter(
            'django_http_requests_total',
            'Total HTTP requests count',
            ['method', 'path', 'status']
        )
        self.REQUEST_DURATION = Histogram(
            'django_http_request_duration_seconds',
            'Request processing time (seconds)',
            ['method', 'path'],
            buckets=[0.01, 0.05, 0.1, 0.5, 1, 2, 5]
        )
        
        # Метрики посещений
        self.PAGE_VISITS = Counter(
            'django_page_visits_total',
            'Total page visits count',
            ['path']
        )
        self.ERRORS_404 = Counter(
            'django_errors_404_total',
            'Total 404 errors count',
            ['path']
        )
        
        # Метрики аутентификации
        self.LOGIN_SUCCESS = Counter(
            'MyMetric_django_login_success_total',
            'Total successful logins count',
            ['user_id', 'role']
        )
        self.LOGIN_FAILED = Counter(
            'django_login_failed_total',
            'Total failed logins count',
            ['reason']
        )
        
        # Метрики базы данных
        self.DB_QUERIES = Counter(
            'django_db_queries_total',
            'Total database queries count',
            ['model', 'operation']
        )
        self.ACTIVE_SESSIONS = Gauge(
            'django_active_sessions_count',
            'Current active sessions count'
        )
    
    def update_system_metrics(self):
        """Обновление системных метрик"""
        self.SYSTEM_CPU.set(psutil.cpu_percent())
        self.PROCESS_CPU.set(psutil.Process().cpu_percent(interval=0.1))
        
        load = psutil.getloadavg()
        self.LOAD_AVG.labels(period='1min').set(load[0])
        self.LOAD_AVG.labels(period='5min').set(load[1])
        self.LOAD_AVG.labels(period='15min').set(load[2])
        
        self.RAM_USAGE.set(psutil.virtual_memory().percent)
        
metrics = DjangoMetrics()

class PrometheusMetricsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._prometheus_start_time = time.time()
        return None
    def process_response(self, request, response):
        metrics.update_system_metrics()
        if hasattr(request, '_prometheus_start_time'):
            duration = time.time() - request._prometheus_start_time
            metrics.REQUEST_DURATION.labels(
                method=request.method,
                path=self._clean_path(request.path)).observe(duration)
        metrics.REQUEST_COUNT.labels(
            method=request.method,
            path=self._clean_path(request.path),
            status=response.status_code
        ).inc()
        if response.status_code == 200 and not request.path.startswith(('/api', '/static')):
            metrics.PAGE_VISITS.labels(
                path=self._clean_path(request.path)).inc()
        if response.status_code == 404:
            metrics.ERRORS_404.labels(
                path=self._clean_path(request.path)
            ).inc()
        return response
    def _clean_path(self, path):
        """Нормализация путей для метрик"""
        patterns = [
            '/api/v1/items/',
            '/user/',
            '/product/',
            '/category/'
        ]
        for pattern in patterns:
            if path.startswith(pattern):
                return f"{pattern}{{id}}"
        return path





















#InfluxDB
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import psutil
import os

# Настройки InfluxDB
INFLUXDB_URL = os.getenv('INFLUXDB_URL', 'http://localhost:8086')
INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN', 'AN0s_moZ0YLY_zP6RTlzTQiFqkDwfiNsWu-D_O-OmBETCBMqBJrB59kTxygPlZOs32HuIgrkKJQaV_Lt_mm5Og==')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG', 'MPT')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET', 'inf')

# Инициализация клиента InfluxDB
influxdb_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

def write_metric(measurement, tags, fields):
    point = Point(measurement)
    for key, value in tags.items():
        point.tag(key, value)
    for key, value in fields.items():
        point.field(key, value)
    write_api.write(bucket=INFLUXDB_BUCKET, record=point)

class PageNotFoundMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            tags = {
                "path": request.path,  # Полный путь запроса
                "method": request.method,  # HTTP-метод (GET, POST и т.д.)
                "status_code": "404",  # Можно добавить статус для группировки
            }
            fields = {
                "count": 1
            }
            write_metric("page_not_found", tags, fields)
        return response
    
class TemplateErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except TemplateSyntaxError as e:
            view_name = request.resolver_match.view_name if hasattr(request, 'resolver_match') else 'unknown'
            tags = {
                "view": view_name
            }
            fields = {
                "count": 1
            }
            write_metric("template_syntax_error", tags, fields)
            raise  
        return response

from prometheus_client import Gauge

# Инициализация метрики на уровне модуля (глобально)
active_requests = Gauge(
    'app_active_requests', 
    'Number of currently processing requests'
)

class ActiveRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Увеличиваем счетчик при поступлении запроса
        active_requests.inc()

        try:
            response = self.get_response(request)
            return response
        finally:
            # Гарантированно уменьшаем счетчик при завершении обработки
            active_requests.dec()

from django.contrib.sessions.models import Session

class ActiveSessionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        active_sessions_count = Session.objects.count()
        tags = {}
        fields = {
            "count": active_sessions_count
        }
        write_metric("active_sessions", tags, fields)
        response = self.get_response(request)

        return response

def update_cpu_metrics():
    """Обновляет метрики, связанные с CPU."""
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_count = psutil.cpu_count(logical=True)
    load_avg = psutil.getloadavg()
    process = psutil.Process()
    process_cpu_usage = process.cpu_percent(interval=0.1)

    tags = {}
    fields = {
        "cpu_percent": cpu_percent,
        "cpu_count": cpu_count,
        "load_avg": load_avg[0],
        "process_cpu_usage": process_cpu_usage
    }
    write_metric("cpu_metrics", tags, fields)

class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        update_cpu_metrics()
        response = self.get_response(request)

        return response
    
