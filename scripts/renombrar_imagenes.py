import os
import shutil
from datetime import datetime

# Extensiones de imagen soportadas (en minúsculas)
EXTENSIONES = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

def crear_carpeta_si_no_existe(ruta_carpeta):
    """Crea una carpeta si no existe"""
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        print(f"📁 Carpeta creada: {ruta_carpeta}")
    return ruta_carpeta

def main():
    print("🔍 Buscando imágenes para renombrar y organizar...")
    print("ℹ️ Se usará la fecha de MODIFICACIÓN del archivo")
    print("ℹ️ Las imágenes se organizarán en carpetas por año\n")
    
    # Contador de archivos procesados
    archivos_procesados = 0
    
    for nombre in os.listdir('.'):
        # Verificar si es una imagen (ignorando mayúsculas)
        if not nombre.lower().endswith(EXTENSIONES):
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
        
        # Mostrar información
        print(f"📄 Archivo: {nombre}")
        print(f"   📅 Fecha modificación: {fecha_modificacion.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   📁 Carpeta destino: {carpeta_año}/")
        print(f"   🏷️  Nuevo nombre: {nuevo_nombre}")

        # Saltar si el archivo ya existe en destino con el mismo nombre
        if os.path.exists(ruta_destino):
            print(f"   ⚠️  Ya existe en destino, se omite: {nuevo_nombre}")
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
    
    print(f"¡Finalizado! Se procesaron {archivos_procesados} archivos.")
    print("Las imágenes se han organizado en carpetas por año.")

if __name__ == "__main__":
    main()