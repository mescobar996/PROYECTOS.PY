# 🗃️ PROYECTOS.PY - Suite Organizadora de Archivos

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-brightgreen.svg)](https://github.com/tu-usuario/PROYECTOS.PY)

Una colección de scripts Python para organizar automáticamente archivos multimedia, limpiar espacio y monitorear tu sistema.

## ✨ Características

- 🖼️ **Organizador de Imágenes**: Clasifica por fecha de modificación
- 🎥 **Organizador de Videos**: Organiza por año con información de tamaño
- 📁 **Clasificador por Tipo**: Organiza documentos, música, archivos, etc.
- 🧹 **Limpieza Inteligente**: Elimina archivos temporales con seguridad
- 📊 **Monitor de Sistema**: Alertas de uso de CPU, memoria y disco
- ⚡ **Rápido y Eficiente**: Procesamiento optimizado
- 🛡️ **Seguro**: Modo simulación y confirmaciones interactivas

## 📦 Scripts Incluidos

| Script | Descripción | Comando |
|--------|-------------|---------|
| `renombrar_imagenes.py` | Organiza imágenes por fecha | `python scripts/renombrar_imagenes.py` |
| `organizar_videos.py` | Organiza videos por año | `python scripts/organizar_videos.py` |
| `file_organizer.py` | Clasifica archivos por tipo | `python scripts/file_organizer.py ~/Downloads` |
| `file_cleaner.py` | Limpieza segura de archivos | `python scripts/file_cleaner.py ~/Downloads --dry-run` |
| `system_health.py` | Monitor del sistema | `python scripts/system_health.py --interval 60` |

## 🚀 Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/PROYECTOS.PY.git
cd PROYECTOS.PY

# Instalar dependencias
pip install -r requirements.txt

# O instalar manualmente
pip install psutil plyer colorama

💡 Uso Rápido
Para organizar imágenes:
bash
cd /ruta/a/tus/fotos
python /ruta/a/PROYECTOS.PY/scripts/renombrar_imagenes.py
Para organizar videos:
bash
cd /ruta/a/tus/videos
python /ruta/a/PROYECTOS.PY/scripts/organizar_videos.py
Para limpiar archivos temporales:
bash
# Modo simulación (recomendado primero)
python scripts/file_cleaner.py ~/Downloads --dry-run

# Limpieza real
python scripts/file_cleaner.py ~/Downloads --days 30

⚙️ Configuración
Archivos de configuración incluidos:
configs/config_organizer.json - Categorías y extensiones

configs/config_cleaner.json - Reglas de limpieza

Personalizar configuración:
bash
# Copiar configuraciones de ejemplo
cp configs/config_organizer.json config_local.json

# Editar con tus preferencias
nano config_local.json

# Usar configuración personalizada
python scripts/file_organizer.py ~/Downloads --config config_local.json

🛡️ Características de Seguridad
✅ Modo Dry-Run: Simula cambios sin afectar archivos

✅ Confirmaciones Interactivas: Pregunta antes de cada acción

✅ Backups Automáticos: Crea copias de seguridad

✅ Logs Detallados: Registro de todas las operaciones

✅ Scripts de Restauración: Permite revertir cambios

📁 Estructura del Proyecto
text
PROYECTOS.PY/
├── 📁 scripts/           # Scripts principales
├── 📁 configs/          # Configuraciones de ejemplo
├── 📁 docs/            # Documentación detallada
├── 📄 requirements.txt  # Dependencias de Python
├── 📄 README.md        # Este archivo
├── 📄 .gitignore       # Archivos ignorados por Git
└── 📄 LICENSE          # Licencia MIT

🐛 Solución de Problemas
Error: "Módulo no encontrado"
bash
# Instalar dependencias faltantes
pip install psutil plyer colorama
Error: Permisos denegados
bash
# Dar permisos de ejecución
chmod +x scripts/*.py
Los archivos no se mueven
Verifica que los archivos no estén en uso

Comprueba que haya espacio en disco

Usa --dry-run para diagnosticar

🔄 Actualizar
bash
# Navegar al directorio del proyecto
cd PROYECTOS.PY

# Obtener últimas actualizaciones
git pull origin main

# Actualizar dependencias
pip install -r requirements.txt --upgrade

🤝 Contribuir
Las contribuciones son bienvenidas:

Haz Fork del proyecto

Crea una rama: git checkout -b feature/nueva-funcionalidad

Haz commit: git commit -m 'Agregar nueva funcionalidad'

Push: git push origin feature/nueva-funcionalidad

Abre un Pull Request

📊 Logs y Monitoreo
~/.file_cleaner.log - Registro de limpiezas

~/.system_health_monitor.log - Métricas del sistema

Ver logs en tiempo real:

bash
tail -f ~/.file_cleaner.log

⚠️ Advertencias Importantes
Siempre haz backup de tus archivos importantes

Prueba con --dry-run antes de ejecutar por primera vez

Supervisa el proceso especialmente con archivos críticos

Los cambios son permanentes - usa los scripts de restauración si es necesario

📄 Licencia
Este proyecto está bajo la Licencia MIT. Ver LICENSE para más detalles.

🆘 Soporte
Si encuentras problemas:

Revisa los archivos de log

Consulta la documentación en docs/instrucciones.md

Abre un issue en GitHub
