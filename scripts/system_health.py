#!/usr/bin/env python3
"""
system_health_monitor.py
Monitor de salud del sistema con notificaciones y logging opcional.
Uso:
    python system_health_monitor.py
    python system_health_monitor.py --interval 30 --cpu 70 --memory 70 --disk 85
"""
import argparse
import logging
import os
import signal
import sys
import time
from typing import NamedTuple

import psutil
from plyer import notification

__version__ = "2.0.0"

# --------------------------------------------------------------------------- #
# Configuración
# --------------------------------------------------------------------------- #
LOG_FILE = os.path.expanduser("~/.system_health_monitor.log")
DEFAULT_INTERVAL = 60
DEFAULT_THRESHOLDS = {"cpu": 80, "memory": 80, "disk": 80}

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

# --------------------------------------------------------------------------- #
# Modelo de datos
# --------------------------------------------------------------------------- #
class Metrics(NamedTuple):
    cpu: float
    memory: float
    disk: float


# --------------------------------------------------------------------------- #
# Utilidades
# --------------------------------------------------------------------------- #
def get_metrics() -> Metrics:
    """Obtiene los tres indicadores clave."""
    # cpu_percent requiere un “primer tick” para ser preciso
    psutil.cpu_percent(interval=None)
    time.sleep(0.5)
    cpu = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    return Metrics(cpu=cpu, memory=memory, disk=disk)


def send_notification(title: str, message: str) -> None:
    """Envía una notificación de escritorio (silenciosa si falla)."""
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="System Health Monitor",
            timeout=10
        )
    except Exception as exc:
        logging.warning("No se pudo mostrar notificación: %s", exc)


def check_thresholds(m: Metrics, thresholds: dict[str, int]) -> None:
    """Compara métricas con umbrales y alerta si es necesario."""
    alerts = []
    if m.cpu > thresholds["cpu"]:
        alerts.append(f"CPU ({m.cpu:.1f}%)")
    if m.memory > thresholds["memory"]:
        alerts.append(f"Memory ({m.memory:.1f}%)")
    if m.disk > thresholds["disk"]:
        alerts.append(f"Disk ({m.disk:.1f}%)")

    if alerts:
        msg = "High usage detected: " + ", ".join(alerts)
        logging.warning(msg)
        send_notification("System Health Alert", msg)
    else:
        logging.info("All metrics within normal range.")


# --------------------------------------------------------------------------- #
# Loop principal
# --------------------------------------------------------------------------- #
class Monitor:
    def __init__(self, interval: int, thresholds: dict[str, int]) -> None:
        self.interval = interval
        self.thresholds = thresholds
        self.running = True
        # Capturar SIGINT (Ctrl+C) y SIGTERM para apagado elegante
        signal.signal(signal.SIGINT, self._stop)
        signal.signal(signal.SIGTERM, self._stop)

    def _stop(self, signum, frame):
        logging.info("Received signal %s – shutting down gracefully...", signum)
        self.running = False

    def run(self) -> None:
        logging.info("Starting monitor (interval=%ss, thresholds=%s)", self.interval, self.thresholds)
        while self.running:
            try:
                metrics = get_metrics()
                logging.info("Metrics: %s", metrics)
                check_thresholds(metrics, self.thresholds)
            except Exception as e:
                logging.exception("Error while sampling metrics: %s", e)

            # Esperar con posibilidad de salida inmediata
            for _ in range(self.interval):
                if not self.running:
                    break
                time.sleep(1)
        logging.info("Monitor stopped.")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def parse_args():
    parser = argparse.ArgumentParser(description="System Health Monitor")
    parser.add_argument("--interval", type=int, default=DEFAULT_INTERVAL,
                        help="Sampling interval in seconds")
    parser.add_argument("--cpu", type=int, default=DEFAULT_THRESHOLDS["cpu"],
                        help="CPU usage threshold (%)")
    parser.add_argument("--memory", type=int, default=DEFAULT_THRESHOLDS["memory"],
                        help="Memory usage threshold (%)")
    parser.add_argument("--disk", type=int, default=DEFAULT_THRESHOLDS["disk"],
                        help="Disk usage threshold (%)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser.parse_args()


# --------------------------------------------------------------------------- #
# Entry-point
# --------------------------------------------------------------------------- #
def main():
    args = parse_args()
    thresholds = {"cpu": args.cpu, "memory": args.memory, "disk": args.disk}
    monitor = Monitor(interval=args.interval, thresholds=thresholds)
    monitor.run()


if __name__ == "__main__":
    main()