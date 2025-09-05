#!/usr/bin/env python3
"""
file_cleaner.py
Script portable y seguro para limpiar archivos temporales, vacíos o según reglas.
Autor: Tu Nombre
Licencia: MIT
Requisitos: Python ≥3.7  (pip install colorama opcional)
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Dict, List

try:
    from colorama import Fore, Style, init as colorama_init  # type: ignore
    colorama_init(autoreset=True)
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RESET = Style.RESET_ALL
except ImportError:
    RED = GREEN = YELLOW = RESET = ""

# --------------------------------------------------------------------------- #
# CONFIGURACIÓN POR DEFECTO
# --------------------------------------------------------------------------- #
DEFAULT_PATTERNS = [
    "*~", "*.tmp", "*.temp", "*.log", "*.bak", "*.old",
    "Thumbs.db", ".DS_Store", ".thumb"
]
DEFAULT_EXCLUDE: List[str] = []
DEFAULT_MIN_DAYS = 7
DEFAULT_MAX_SIZE_KB = 0  # 0 = sin límite de tamaño

# --------------------------------------------------------------------------- #
# LOGGING
# --------------------------------------------------------------------------- #
LOG_PATH = Path.home() / ".file_cleaner.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# --------------------------------------------------------------------------- #
# UTILIDADES
# --------------------------------------------------------------------------- #
def confirm(prompt: str) -> bool:
    """Pregunta y/n al usuario."""
    try:
        return input(f"{prompt} [y/N]: ").strip().lower() == "y"
    except (KeyboardInterrupt, EOFError):
        return False

def size_in_kb(path: Path) -> float:
    """Devuelve tamaño en KB."""
    return path.stat().st_size / 1024

def matches_any(name: str, patterns: List[str]) -> bool:
    """True si 'name' coincide con algún patrón glob."""
    from fnmatch import fnmatch
    return any(fnmatch(name, pat) for pat in patterns)

def build_restore_script(files: List[Path], base: Path) -> Path:
    """Genera .sh / .bat para restaurar archivos borrados."""
    ts = int(time.time())
    ext = "bat" if os.name == "nt" else "sh"
    script_path = base / f"restore_{ts}.{ext}"

    lines = []
    if ext == "sh":
        lines.append("#!/bin/bash")
        for f in files:
            dest = f.parent
            lines.append(f'mkdir -p "{dest}" && mv "{f}.bak" "{f}"')
    else:
        for f in files:
            dest = f.parent
            lines.append(f'if not exist "{dest}" mkdir "{dest}"')
            lines.append(f'move /y "{f}.bak" "{f}"')

    script_path.write_text("\n".join(lines), encoding="utf-8")
    if ext == "sh":
        os.chmod(script_path, 0o755)
    logging.info("Script de restauración: %s", script_path)
    return script_path

# --------------------------------------------------------------------------- #
# CLASE PRINCIPAL
# --------------------------------------------------------------------------- #
class Cleaner:
    def __init__(
        self,
        folder: Path,
        patterns: List[str] = None,
        exclude: List[str] = None,
        min_days: int = DEFAULT_MIN_DAYS,
        max_size_kb: float = DEFAULT_MAX_SIZE_KB,
        dry_run: bool = True,
        interactive: bool = False
    ) -> None:
        self.folder = folder.expanduser().resolve()
        self.patterns = patterns or DEFAULT_PATTERNS
        self.exclude = exclude or DEFAULT_EXCLUDE
        self.min_days = min_days
        self.max_size_kb = max_size_kb
        self.dry_run = dry_run
        self.interactive = interactive
        self.to_delete: List[Path] = []
        self.deleted: List[Path] = []

    # ....................................................................... #
    def scan(self) -> None:
        """Llena la lista de archivos a borrar según filtros."""
        now = time.time()
        cutoff = now - (self.min_days * 86400)

        for item in self.folder.rglob("*"):
            if not item.is_file():
                continue
            if matches_any(item.name, self.exclude):
                continue
            if not matches_any(item.name, self.patterns) and self.max_size_kb <= 0:
                continue
            if item.stat().st_mtime < cutoff:
                if self.max_size_kb > 0 and size_in_kb(item) > self.max_size_kb:
                    continue
                self.to_delete.append(item)

        logging.info("Archivos a borrar: %d", len(self.to_delete))

    # ....................................................................... #
    def run(self) -> None:
        if not self.folder.exists():
            logging.error("La carpeta %s no existe.", self.folder)
            return

        self.scan()
        if not self.to_delete:
            logging.info("Nada que borrar.")
            return

        if self.dry_run:
            logging.info("Modo DRY-RUN – no se borra nada.")
            for f in self.to_delete:
                print(f"{YELLOW}DRY-RUN{RESET} -> {f}")
            return

        if self.interactive:
            for f in self.to_delete:
                if confirm(f"Borrar {f}?"):
                    self._delete(f)
        else:
            if not confirm(f"Borrar {len(self.to_delete)} archivos?"):
                logging.info("Cancelado por el usuario.")
                return
            for f in self.to_delete:
                self._delete(f)

        if self.deleted:
            build_restore_script(self.deleted, self.folder)

    # ....................................................................... #
    def _delete(self, file_path: Path) -> None:
        """Mueve a .bak y luego borra; permite rollback."""
        try:
            bak = file_path.with_suffix(file_path.suffix + ".bak")
            shutil.move(file_path, bak)
            bak.unlink(missing_ok=True)
            self.deleted.append(file_path)
            print(f"{GREEN}Borrado{RESET}: {file_path}")
        except Exception as e:
            logging.error("Error al borrar %s: %s", file_path, e)

# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def load_config(config_path: Path) -> Dict:
    try:
        with open(config_path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error("Error leyendo config: %s", e)
        sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser(description="Limpia archivos temporales y basura.")
    parser.add_argument("folder", help="Carpeta a limpiar")
    parser.add_argument("--dry-run", action="store_true", help="Simular sin borrar")
    parser.add_argument("--confirm", action="store_true", help="Preguntar antes de borrar")
    parser.add_argument("--config", type=Path, help="Archivo JSON con reglas")
    parser.add_argument("--days", type=int, default=DEFAULT_MIN_DAYS,
                        help="Mínimo días de antigüedad (default 7)")
    parser.add_argument("--size", type=float, default=DEFAULT_MAX_SIZE_KB,
                        help="Máximo tamaño KB a borrar (0 = sin límite)")
    parser.add_argument("--ext", help="Extensiones extra separadas por coma (sin punto)")
    return parser.parse_args()

# --------------------------------------------------------------------------- #
# ENTRY-POINT
# --------------------------------------------------------------------------- #
def main():
    args = parse_args()
    folder = Path(args.folder)

    patterns = DEFAULT_PATTERNS.copy()
    exclude = DEFAULT_EXCLUDE.copy()
    min_days = args.days
    max_size = args.size

    if args.config:
        cfg = load_config(args.config)
        patterns = cfg.get("patterns", patterns)
        exclude = cfg.get("exclude", exclude)
        min_days = cfg.get("min_days", min_days)
        max_size = cfg.get("max_size_kb", max_size)

    if args.ext:
        patterns.extend(f"*.{ext.strip()}" for ext in args.ext.split(","))

    cleaner = Cleaner(
        folder=folder,
        patterns=patterns,
        exclude=exclude,
        min_days=min_days,
        max_size_kb=max_size,
        dry_run=not (args.confirm or False),
        interactive=args.confirm
    )
    cleaner.run()

if __name__ == "__main__":
    main()