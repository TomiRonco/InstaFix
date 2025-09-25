#!/usr/bin/env python3
"""
InstaFix - Build Script para Windows
Genera ejecutables para distribución en Windows
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import platform

def print_header():
    """Mostrar encabezado del script"""
    print("🚀 InstaFix - Generador de Instalador para Windows")
    print("=" * 55)

def check_dependencies():
    """Verificar dependencias necesarias"""
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
        return True
    except ImportError:
        print("❌ PyInstaller no encontrado")
        print("💡 Instala con: pip install pyinstaller")
        return False

def create_pyinstaller_spec_windows():
    """Crear archivo .spec para PyInstaller específico para Windows"""
    spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['{os.getcwd()}'],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('.env.example', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'ttkbootstrap',
        'reportlab',
        'reportlab.pdfgen',
        'reportlab.lib',
        'reportlab.platypus',
        'reportlab.graphics',
        'sqlite3',
        'webbrowser',
        'urllib.parse',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'requests',
        'os',
        'sys',
        'logging',
        'datetime',
        'json',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='InstaFix.exe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
'''
    
    with open('InstaFix_Windows.spec', 'w') as f:
        f.write(spec_content)
    print("✅ Archivo InstaFix_Windows.spec creado")

def build_executable_windows():
    """Construir el ejecutable usando PyInstaller para Windows"""
    print("🔨 Construyendo ejecutable para Windows...")
    
    # Ejecutar PyInstaller con el archivo .spec
    result = subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        'InstaFix_Windows.spec'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Ejecutable Windows creado exitosamente")
        return True
    else:
        print("❌ Error al crear ejecutable:")
        print(result.stdout)
        print(result.stderr)
        return False

def create_installer_package_windows():
    """Crear paquete de instalación específico para Windows"""
    package_dir = Path("InstaFix_Installer_Windows")
    
    # Crear directorio del instalador
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copiar ejecutable
    exe_source = Path("dist/InstaFix.exe")
    exe_dest = package_dir / "InstaFix.exe"
    
    if exe_source.exists():
        shutil.copy2(exe_source, exe_dest)
        print(f"✅ Ejecutable copiado a {exe_dest}")
    else:
        print("❌ No se encontró el ejecutable InstaFix.exe")
        return False
    
    # Copiar archivos de configuración
    config_files = ['.env.example', 'requirements.txt']
    for file in config_files:
        if os.path.exists(file):
            shutil.copy2(file, package_dir / file)
            print(f"✅ {file} copiado")
    
    # Crear README específico para Windows
    readme_content = """# InstaFix - Instalación para Windows

## Instrucciones de Instalación

### Requisitos del Sistema
- Windows 10 o superior
- No requiere Python instalado

### Pasos de Instalación

1. **Extraer archivos:**
   - Extrae todos los archivos del ZIP en una carpeta de tu elección
   - Recomendado: `C:\\Program Files\\InstaFix\\` o `C:\\InstaFix\\`

2. **Configuración inicial:**
   - Copia el archivo `.env.example` y renómbralo como `.env`
   - Haz clic derecho en `.env` → "Abrir con" → "Bloc de notas"
   - Edita el archivo con los datos de tu negocio:
     ```
     BUSINESS_NAME=Tu Nombre del Negocio
     BUSINESS_ADDRESS=Tu Dirección Completa
     BUSINESS_PHONE=Tu Teléfono Fijo
     BUSINESS_MOBILE=Tu Celular
     BUSINESS_EMAIL=tu@email.com
     ```
   - Guarda y cierra el archivo

3. **Ejecutar la aplicación:**
   - Doble clic en `InstaFix.exe`
   - La primera vez puede tardar un poco en iniciar (30-60 segundos)
   - Se creará automáticamente la base de datos

4. **Crear acceso directo (Opcional):**
   - Clic derecho en `InstaFix.exe` → "Crear acceso directo"
   - Mueve el acceso directo al Escritorio o al menú Inicio

## Características

- ✅ Gestión completa de reparaciones
- ✅ Generación de PDFs profesionales
- ✅ Integración con WhatsApp Web
- ✅ Interface moderna y responsive
- ✅ Base de datos SQLite integrada
- ✅ Sin necesidad de instalar Python
- ✅ Compatible con Windows 10/11

## Solución de Problemas

### Si no abre la aplicación:
1. Asegúrate que Windows no esté bloqueando el archivo
2. Clic derecho en InstaFix.exe → "Propiedades" → "Desbloquear" (si aparece)
3. Ejecuta como Administrador (clic derecho → "Ejecutar como administrador")

### Si aparece error de antivirus:
- Agrega la carpeta de InstaFix a las excepciones de tu antivirus
- Es normal que algunos antivirus marquen ejecutables de PyInstaller como sospechosos

### Para reportar problemas:
- GitHub: https://github.com/TomiRonco/InstaFix
- Email: soporte@instafix.com

## Versión

- Versión: 1.0.0 Windows Edition
- Fecha: 24 de septiembre de 2025
- Plataforma: Windows x64
- Python: No requerido
"""
    
    readme_path = package_dir / "README_Windows.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✅ README_Windows.md creado")
    
    # Crear archivo batch para facilitar la ejecución
    bat_content = '''@echo off
echo Iniciando InstaFix...
echo Por favor espera, puede tardar un momento en cargar...
start "" "InstaFix.exe"
'''
    
    bat_path = package_dir / "Ejecutar_InstaFix.bat"
    with open(bat_path, 'w', encoding='utf-8') as f:
        f.write(bat_content)
    print("✅ Ejecutar_InstaFix.bat creado")
    
    print(f"✅ Paquete de instalación Windows creado en: {package_dir.absolute()}")
    return True

def create_zip_package():
    """Crear archivo ZIP para distribución"""
    try:
        # Crear nombre del ZIP con timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d")
        zip_name = f"InstaFix_v1.0.0_Windows_{timestamp}.zip"
        
        # Comprimir usando shutil
        base_name = zip_name.replace('.zip', '')
        shutil.make_archive(base_name, 'zip', 'InstaFix_Installer_Windows')
        
        print(f"✅ Archivo ZIP creado: {zip_name}")
        
        # Mostrar tamaño del archivo
        if os.path.exists(zip_name):
            size_mb = os.path.getsize(zip_name) / (1024 * 1024)
            print(f"📦 Tamaño: {size_mb:.1f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando ZIP: {e}")
        return False

def cleanup():
    """Limpiar archivos temporales"""
    try:
        # Limpiar archivos de build
        temp_dirs = ['build', '__pycache__']
        for dir_name in temp_dirs:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
        
        # Limpiar archivos .spec temporales
        if os.path.exists('InstaFix_Windows.spec'):
            os.remove('InstaFix_Windows.spec')
            
        print("🧹 Archivos temporales eliminados")
        
    except Exception as e:
        print(f"⚠️  Error limpiando archivos temporales: {e}")

def main():
    """Función principal"""
    try:
        print_header()
        
        # Verificar que estamos en el directorio correcto
        if not os.path.exists('main.py'):
            print("❌ No se encontró main.py")
            print("💡 Ejecuta este script desde el directorio raíz del proyecto")
            return False
        
        # Verificar dependencias
        if not check_dependencies():
            return False
        
        # Crear archivo .spec
        create_pyinstaller_spec_windows()
        
        # Construir ejecutable
        if not build_executable_windows():
            return False
        
        # Crear paquete de instalación
        if not create_installer_package_windows():
            return False
            
        # Crear ZIP para distribución
        create_zip_package()
        
        # Limpiar archivos temporales
        cleanup()
        
        print("\n🎉 ¡Instalador para Windows creado exitosamente!")
        print(f"📁 Ubicación: {os.path.abspath('InstaFix_Installer_Windows')}")
        print("\n📋 Próximos pasos:")
        print("1. Comparte el archivo ZIP generado")
        print("2. Los usuarios deben extraer y seguir el README_Windows.md")
        print("3. No requieren Python instalado")
        
        return True
        
    except KeyboardInterrupt:
        print("\n⏹️  Proceso cancelado por el usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)