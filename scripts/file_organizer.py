#!/usr/bin/env python3
"""
file_organizer.py
Organiza archivos por tipo en carpetas. Seguro, portable y con CLI.

Uso:
    python file_organizer.py ~/Downloads
    python file_organizer.py --dry-run ~/Downloads
    python file_organizer.py --config my_config.json ~/Downloads
"""
import argparse
import json
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List

__version__ = "2.0.0"

# --------------------------------------------------------------------------- #
# Configuración por defecto
# --------------------------------------------------------------------------- #
DEFAULT_MAPPING: Dict[str, List[str]] = {
    "Documents": [
        ".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt", ".xls", ".xlsx", ".csv"
    ],
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"
    ],
    "Videos": [
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v"
    ],
    "Music": [
        ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"
    ],
    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"
    ],
    "Scripts": [
        ".py", ".js", ".sh", ".bat", ".ps1", ".rb", ".pl"
    ],
}

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# --------------------------------------------------------------------------- #
# Core
# --------------------------------------------------------------------------- #
class Organizer:
    def __init__(
        self,
        base: Path,
        mapping: Dict[str, List[str]],
        dry_run: bool = False
    ) -> None:
        self.base = Path(base).expanduser().resolve()
        self.mapping = {k: [ext.lower() for ext in v] for k, v in mapping.items()}
        self.dry_run = dry_run
        self._created_dirs: set[Path] = set()

    # ....................................................................... #
    def run(self) -> None:
        if not self.base.exists():
            logging.error("La carpeta %s no existe.", self.base)
            return

        logging.info("Escaneando %s", self.base)
        files = [p for p in self.base.iterdir() if p.is_file()]
        logging.info("Archivos encontrados: %d", len(files))

        for file in files:
            self._process_file(file)

        logging.info("Proceso finalizado.")

    # ....................................................................... #
    def _process_file(self, file: Path) -> None:
        ext = file.suffix.lower()
        target_folder_name = next(
            (folder for folder, exts in self.mapping.items() if ext in exts),
            "Others"
        )
        target_folder = self.base / target_folder_name
        target_path = target_folder / file.name

        if target_path.exists():
            logging.warning("Conflicto: ya existe %s – se omite.", target_path)
            return

        if self.dry_run:
            logging.info("[DRY-RUN] %s -> %s", file, target_path)
            return

        # Crear carpeta destino si hace falta
        target_folder.mkdir(exist_ok=True)
        self._created_dirs.add(target_folder)

        try:
            shutil.move(str(file), str(target_path))
            logging.info("Movido: %s -> %s", file.name, target_folder_name)
        except Exception as exc:
            logging.exception("Error al mover %s: %s", file, exc)

# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def parse_args():
    parser = argparse.ArgumentParser(description="Organiza archivos por tipo.")
    parser.add_argument("folder", help="Carpeta a organizar")
    parser.add_argument(
        "--config",
        help="JSON con mapeo personalizado",
        type=Path,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula el movimiento sin tocar archivos",
    )
    parser.add_argument("--version", action="version", version=__version__)
    return parser.parse_args()


def load_mapping(config_path: Path | None) -> Dict[str, List[str]]:
    if config_path is None:
        return DEFAULT_MAPPING
    try:
        with open(config_path, encoding="utf-8") as f:
            mapping = json.load(f)
        logging.info("Configuración personalizada cargada.")
        return mapping
    except Exception as exc:
        logging.error("Error leyendo %s: %s – usando mapeo por defecto.", config_path, exc)
        return DEFAULT_MAPPING


# --------------------------------------------------------------------------- #
# Entry-point
# --------------------------------------------------------------------------- #
def main():
    args = parse_args()
    mapping = load_mapping(args.config)
    organizer = Organizer(args.folder, mapping, dry_run=args.dry_run)
    organizer.run()


if __name__ == "__main__":
    main()