import logging
import sys
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# from opentelemetry.sdk.logs import LoggingHandler, LogEmitterProvider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
# from opentelemetry.sdk.logs.export import BatchLogRecordProcessor
from opentelemetry.sdk._logs import LoggingHandler, LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.instrumentation.logging import LoggingInstrumentor


def setup_otel(service_name: str):
    # --- Ресурсы (имя сервиса) ---
    resource = Resource(attributes={
        SERVICE_NAME: service_name
    })

    # --- Настройка трейсинга ---
    trace_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(trace_provider)

    # Экспорт трейсов в OTEL Collector (HTTP OTLP)
    trace_exporter = OTLPSpanExporter(
        endpoint="http://otel-collector:4318/v1/traces",
    )
    trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))

    # --- Настройка логирования ---
    log_provider = LoggerProvider(resource=resource)
    log_exporter = OTLPLogExporter(
        endpoint="http://vector:4318/v1/logs",
    )
    log_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

    # --- Python logging ---
    LoggingInstrumentor().instrument(set_logging_format=True)

    # Добавляем обработчик, который будет писать логи и в stdout, и в OTEL
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] trace_id=%(otelTraceID)s span_id=%(otelSpanID)s %(name)s: %(message)s",
        stream=sys.stdout
    )
    handler = LoggingHandler(level=logging.INFO, logger_provider=log_provider)
    logging.getLogger().addHandler(handler)

    logging.getLogger(__name__).info(f"OpenTelemetry initialized for {service_name}")