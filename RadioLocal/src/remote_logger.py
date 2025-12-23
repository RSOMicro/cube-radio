import logging
from fluent import handler as fluent_handler
import sys
from pathlib import Path

def get_service_name():
    return Path(__file__).resolve().parents[1].name
	
class ServiceNameFilter(logging.Filter):
    def __init__(self, service_name: str):
        super().__init__()
        self.service_name = service_name

    def filter(self, record: logging.LogRecord) -> bool:
        record.service_name = self.service_name
        return True

def setup_logging():
    service_name = get_service_name()

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    service_filter = ServiceNameFilter(service_name)

    # ---- STDOUT handler (Docker-friendly) ----
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_formatter = logging.Formatter(
        '[%(service_name)s] %(levelname)s:     %(name)s %(message)s'
    )
    stdout_handler.setFormatter(stdout_formatter)
    stdout_handler.addFilter(service_filter)

    # ---- Fluentd handler ----
    fluentd_handler = fluent_handler.FluentHandler(
        tag='fluentd.test',
        host='localhost',
        port=24224
    )

    fluentd_handler.setFormatter(
        fluent_handler.FluentRecordFormatter({
            'level': '%(levelname)s',
            'logger': '%(name)s',
            'message': '%(message)s',
            'timestamp': '%(asctime)s'
        })
    )

    logger.addHandler(stdout_handler)
    logger.addHandler(fluentd_handler)

    return logger