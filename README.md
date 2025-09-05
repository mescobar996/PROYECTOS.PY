🗃️ Suite de Utilidades de Organización y Mantenimiento
Esta colección de scripts Python te ayuda a organizar archivos multimedia, limpiar espacio y monitorear la salud de tu sistema.

📋 Scripts Disponibles
1. 🖼️ renombrar_imagenes.py
Organiza imágenes en carpetas por año según su fecha de modificación.

Formatos soportados: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp

2. 🎥 organizar_videos.py
Organiza videos en carpetas por año según su fecha de modificación.

Formatos soportados: .mp4, .mov, .avi, .wmv, .flv, .webm, .mkv, .m4v, .mpg, .mpeg, .3gp, .3g2, .mts, .m2ts, .vob, .ogv, .divx, .f4v, .m4p

3. 📁 file_organizer.py
Organiza archivos por tipo en carpetas predefinidas.

Categorías por defecto:

Documents: .pdf, .doc, .docx, .odt, .rtf, .txt, .xls, .xlsx, .csv

Images: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .svg, .webp

Videos: .mp4, .mkv, .avi, .mov, .wmv, .flv, .webm, .m4v

Music: .mp3, .wav, .flac, .aac, .ogg, .wma, .m4a

Archives: .zip, .rar, .7z, .tar, .gz, .bz2

Scripts: .py, .js, .sh, .bat, .ps1, .rb, .pl

4. 🧹 file_cleaner.py
Limpia archivos temporales y basura según reglas configurables.

Características:

Patrones predefinidos: *~, *.tmp, *.temp, *.log, *.bak, *.old, Thumbs.db, .DS_Store

Filtros por antigüedad y tamaño

Modo dry-run y confirmación interactiva

Script de restauración automático

5. 📊 system_health.py
Monitor de salud del sistema con alertas y notificaciones.

Métricas monitoreadas:

Uso de CPU (%)

Uso de memoria RAM (%)

Uso de disco (%)

🚀 Instalación y Requisitos
Prerrequisitos
bash
# Python 3.7 o superior
python --version

# Instalar dependencias
pip install psutil plyer colorama
Configuración
Clona o descarga los scripts en una carpeta

Hazlos ejecutables (opcional):

bash
chmod +x *.py
🎯 Uso de los Scripts
Para organizar imágenes:
bash
# Navegar a la carpeta con imágenes
cd /ruta/a/mis/fotos

# Ejecutar el organizador
python renombrar_imagenes.py
Para organizar videos:
bash
cd /ruta/a/mis/videos
python organizar_videos.py
Para organizar archivos por tipo:
bash
python file_organizer.py ~/Downloads
python file_organizer.py ~/Downloads --dry-run  # Simular sin cambios
python file_organizer.py ~/Downloads --config mi_config.json  # Config personalizada
Para limpiar archivos temporales:
bash
python file_cleaner.py ~/Downloads --days 7 --size 1024
python file_cleaner.py ~/Downloads --dry-run  # Solo mostrar qué se borraría
python file_cleaner.py ~/Downloads --confirm  # Confirmar cada borrado
Para monitorear el sistema:
bash
python system_health.py
python system_health.py --interval 30 --cpu 85 --memory 90 --disk 95
⚙️ Configuración Avanzada
Configuración personalizada para file_organizer
Crea un archivo JSON con tu mapeo personalizado:

json
{
    "Documentos": [".pdf", ".docx", ".txt"],
    "Fotos": [".jpg", ".png", ".raw"],
    "Videos": [".mp4", ".mov"],
    "Audio": [".mp3", ".wav", ".flac"]
}
Configuración personalizada para file_cleaner
json
{
    "patterns": ["*.tmp", "*.log", "*.cache"],
    "exclude": ["important.tmp", "backup.log"],
    "min_days": 30,
    "max_size_kb": 5120
}
🛡️ Características de Seguridad
✅ Modo dry-run disponible en todos los scripts

✅ Confirmación interactiva antes de cambios destructivos

✅ Backup automático de archivos eliminados

✅ Scripts de restauración generados automáticamente

✅ Logging detallado de todas las operaciones

📊 Estructura de Carpetas Resultante
Después de ejecutar los organizadores:

text
📂 Directorio_principal/
├── 📂 2023/
│   ├── 🖼️ 20230515_143022.jpg
│   ├── 🎥 20230620_093145.mp4
│   └── 🎥 20231225_162301.mov
├── 📂 2024/
│   ├── 🖼️ 20240110_084511.png
│   └── 🎥 20240214_201530.avi
├── 📂 Documents/
├── 📂 Images/
├── 📂 Videos/
└── 📂 Music/
🐛 Solución de Problemas
Error: "ModuleNotFoundError"
bash
# Instalar dependencias faltantes
pip install psutil plyer colorama
Error: Permisos denegados
bash
# Ejecutar con permisos adecuados
chmod +x script.py
Los archivos no se mueven
Verificar que los archivos no estén en uso por otras aplicaciones

Comprobar que haya espacio suficiente en disco

Usar el modo --dry-run primero para simular

📝 Logs y Monitoreo
file_cleaner.py: Logs en ~/.file_cleaner.log

system_health.py: Logs en ~/.system_health_monitor.log

Todos los scripts muestran output en tiempo real por consola

🔄 Restauración de Cambios
Para recuperar archivos eliminados:
bash
# Ejecutar el script de restauración generado
./restore_1734567890.sh  # Linux/Mac
restore_1734567890.bat   # Windows
Para deshacer organización:
Los scripts de organización no modifican los archivos originales, solo los mueven. Puedes:

Usar el explorador de archivos para moverlos manualmente

Usar comandos de terminal para revertir los cambios

🤝 Contribuir
Si encuentras errores o quieres mejorar estos scripts:

Haz fork del proyecto

Crea una rama para tu feature

Commit tus cambios

Push a la rama

Abre un Pull Request

📄 Licencia
Todos los scripts están bajo licencia MIT. Puedes usarlos, modificarlos y distribuirlos libremente.

⚠️ Advertencias
Siempre haz backup de tus archivos importantes antes de usar scripts de limpieza

Prueba primero con --dry-run para ver qué cambios se realizarán

Supervisa el proceso especialmente la primera vez que uses cada script

Los cambios son permanentes - una vez eliminados los archivos, solo se pueden recuperar con el script de restauración si se generó