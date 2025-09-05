import os
import shutil
from datetime import datetime

# Extensiones de video soportadas (en minúsculas)
EXTENSIONES_VIDEO = (
    '.mp4', '.mov', '.avi', '.wmv', '.flv', '.webm', '.mkv', 
    '.m4v', '.mpg', '.mpeg', '.3gp', '.3g2', '.mts', '.m2ts',
    '.vob', '.ogv', '.divx', '.f4v', '.avi', '.m4p', '.m4v'
)

def crear_carpeta_si_no_existe(ruta_carpeta):
    """Crea una carpeta si no existe"""
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        print(f"📁 Carpeta creada: {ruta_carpeta}")
    return ruta_carpeta

def obtener_tamano_archivo(ruta_archivo):
    """Obtiene el tamaño del archivo en formato legible"""
    tamano_bytes = os.path.getsize(ruta_archivo)
    if tamano_bytes >= 1024 * 1024 * 1024:
        return f"{tamano_bytes/(1024*1024*1024):.2f} GB"
    elif tamano_bytes >= 1024 * 1024:
        return f"{tamano_bytes/(1024*1024):.2f} MB"
    elif tamano_bytes >= 1024:
        return f"{tamano_bytes/1024:.2f} KB"
    else:
        return f"{tamano_bytes} bytes"

def main():
    print("🎥 Buscando videos para renombrar y organizar...")
    print("ℹ️ Se usará la fecha de MODIFICACIÓN del archivo")
    print("ℹ️ Los videos se organizarán en carpetas por año\n")
    
    # Contador de archivos procesados
    archivos_procesados = 0
    archivos_omitidos = 0
    
    for nombre in os.listdir('.'):
        # Verificar si es un video (ignorando mayúsculas)
        if not nombre.lower().endswith(EXTENSIONES_VIDEO):
            continue

        ruta_original = os.path.join('.', nombre)
        if not os.path.isfile(ruta_original):
            continue

        # Obtener fecha de MODIFICACIÓN
        timestamp_modificacion = os.path.getmtime(ruta_original)
        fecha_modificacion = datetime.fromtimestamp(timestamp_modificacion)
        
        # Obtener año para la carpeta
        año = fecha_modificacion.strftime("%Y")
        
        # Crear carpeta del año si no existe
        carpeta_año = crear_carpeta_si_no_existe(año)
        
        # Formatear nuevo nombre
        base = fecha_modificacion.strftime("%Y%m%d_%H%M%S")
        extension = os.path.splitext(nombre)[1].lower()
        nuevo_nombre = f"{base}{extension}"
        
        # Ruta completa del nuevo archivo
        ruta_destino = os.path.join(carpeta_año, nuevo_nombre)
        
        # Obtener tamaño del archivo
        tamano = obtener_tamano_archivo(ruta_original)
        
        # Mostrar información
        print(f"🎬 Video: {nombre}")
        print(f"   📅 Fecha modificación: {fecha_modificacion.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   💾 Tamaño: {tamano}")
        print(f"   📁 Carpeta destino: {carpeta_año}/")
        print(f"   🏷️  Nuevo nombre: {nuevo_nombre}")

        # Saltar si el archivo ya existe en destino con el mismo nombre
        if os.path.exists(ruta_destino):
            print(f"   ⚠️  Ya existe en destino, se omite")
            archivos_omitidos += 1
            print()
            continue

        # Mover y renombrar el archivo
        try:
            shutil.move(ruta_original, ruta_destino)
            print(f"   ✅ Movido a: {carpeta_año}/{nuevo_nombre}")
            archivos_procesados += 1
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        print()
    
    print(f"¡Finalizado! Se procesaron {archivos_procesados} videos.")
    print(f"Se omitieron {archivos_omitidos} videos que ya existían en destino.")
    print("Los videos se han organizado en carpetas por año.")

if __name__ == "__main__":
    main()