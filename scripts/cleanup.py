#!/usr/bin/env python3
"""
InstaFix - Script de Limpieza y Mantenimiento
Limpia archivos temporales y organiza el proyecto
"""

import os
import shutil
import sys
from pathlib import Path

def print_header():
    print("🧹 InstaFix - Script de Limpieza")
    print("=" * 40)

def limpiar_archivos_temporales():
    """Limpiar archivos temporales y de build"""
    print("📁 Limpiando archivos temporales...")
    
    # Archivos y carpetas a limpiar
    temp_items = [
        '__pycache__',
        'build',
        'dist',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.pytest_cache',
        '*.egg-info',
        '.coverage',
        'htmlcov',
        '*.log',
        '*.tmp',
        '*.temp',
        '.DS_Store',
        'Thumbs.db',
        '*.spec'
    ]
    
    cleaned = 0
    
    for item in temp_items:
        if '*' in item:
            # Archivos con wildcard
            import glob
            files = glob.glob(f"**/{item}", recursive=True)
            for file in files:
                try:
                    os.remove(file)
                    print(f"  ✅ Eliminado: {file}")
                    cleaned += 1
                except:
                    pass
        else:
            # Carpetas y archivos específicos
            if os.path.exists(item):
                try:
                    if os.path.isdir(item):
                        shutil.rmtree(item)
                    else:
                        os.remove(item)
                    print(f"  ✅ Eliminado: {item}")
                    cleaned += 1
                except:
                    pass
    
    print(f"✨ {cleaned} elementos eliminados")

def verificar_estructura():
    """Verificar que la estructura del proyecto sea correcta"""
    print("\\n🔍 Verificando estructura del proyecto...")
    
    estructura_esperada = {
        'archivos': [
            'main.py',
            'requirements.txt',
            '.env.example',
            '.gitignore',
            'README.md',
            'LICENSE'
        ],
        'carpetas': [
            'src',
            'src/gui',
            'src/database',
            'src/whatsapp',
            'scripts',
            'docs',
            'releases',
            'assets'
        ]
    }
    
    faltantes = []
    
    # Verificar archivos
    for archivo in estructura_esperada['archivos']:
        if not os.path.exists(archivo):
            faltantes.append(f"📄 {archivo}")
        else:
            print(f"  ✅ {archivo}")
    
    # Verificar carpetas
    for carpeta in estructura_esperada['carpetas']:
        if not os.path.exists(carpeta):
            faltantes.append(f"📁 {carpeta}")
        else:
            print(f"  ✅ {carpeta}/")
    
    if faltantes:
        print("\\n⚠️  Elementos faltantes:")
        for item in faltantes:
            print(f"  ❌ {item}")
        return False
    else:
        print("\\n✨ Estructura del proyecto correcta")
        return True

def crear_estructura_faltante():
    """Crear carpetas faltantes"""
    carpetas_requeridas = [
        'src',
        'src/gui',
        'src/database', 
        'src/whatsapp',
        'scripts',
        'docs',
        'releases',
        'assets'
    ]
    
    print("\\n🏗️  Creando estructura faltante...")
    
    for carpeta in carpetas_requeridas:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta, exist_ok=True)
            print(f"  ✅ Creada: {carpeta}/")
            
            # Crear __init__.py en carpetas de Python
            if carpeta.startswith('src/'):
                init_file = os.path.join(carpeta, '__init__.py')
                if not os.path.exists(init_file):
                    with open(init_file, 'w') as f:
                        f.write('# InstaFix module\\n')
                    print(f"  ✅ Creado: {init_file}")

def validar_archivos_principales():
    """Validar que los archivos principales existan y tengan contenido"""
    print("\\n🔧 Validando archivos principales...")
    
    archivos_criticos = {
        'main.py': 'if __name__ == "__main__"',
        'requirements.txt': 'tkinter',
        '.env.example': 'BUSINESS_NAME',
        'README.md': '# InstaFix'
    }
    
    for archivo, contenido_esperado in archivos_criticos.items():
        if os.path.exists(archivo):
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    if contenido_esperado in contenido:
                        print(f"  ✅ {archivo} - OK")
                    else:
                        print(f"  ⚠️  {archivo} - Contenido incompleto")
            except:
                print(f"  ❌ {archivo} - Error de lectura")
        else:
            print(f"  ❌ {archivo} - No existe")

def mostrar_estadisticas():
    """Mostrar estadísticas del proyecto"""
    print("\\n📊 Estadísticas del proyecto:")
    
    # Contar archivos Python
    python_files = list(Path('.').rglob('*.py'))
    print(f"  📝 Archivos Python: {len(python_files)}")
    
    # Contar líneas de código
    total_lines = 0
    for file in python_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                total_lines += len(f.readlines())
        except:
            pass
    print(f"  📏 Líneas de código: {total_lines}")
    
    # Tamaño del proyecto
    total_size = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            try:
                total_size += os.path.getsize(os.path.join(root, file))
            except:
                pass
    
    size_mb = total_size / (1024 * 1024)
    print(f"  💾 Tamaño total: {size_mb:.1f} MB")
    
    # Archivos de documentación
    doc_files = list(Path('docs').glob('*.md')) if os.path.exists('docs') else []
    print(f"  📚 Archivos de documentación: {len(doc_files)}")

def main():
    """Función principal del script de limpieza"""
    try:
        print_header()
        
        # Verificar que estamos en el directorio correcto
        if not os.path.exists('main.py'):
            print("❌ Este script debe ejecutarse desde el directorio raíz de InstaFix")
            return False
        
        # Ejecutar tareas de limpieza
        limpiar_archivos_temporales()
        crear_estructura_faltante()
        
        # Verificar estructura
        estructura_ok = verificar_estructura()
        
        # Validar archivos
        validar_archivos_principales()
        
        # Mostrar estadísticas
        mostrar_estadisticas()
        
        print("\\n🎉 Limpieza completada!")
        
        if estructura_ok:
            print("✅ Proyecto listo para desarrollo o distribución")
        else:
            print("⚠️  Revisa los elementos faltantes antes de continuar")
        
        return True
        
    except KeyboardInterrupt:
        print("\\n⏹️  Limpieza cancelada por el usuario")
        return False
    except Exception as e:
        print(f"\\n❌ Error durante la limpieza: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)