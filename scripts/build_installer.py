#!/usr/bin/env python3
"""
Script para crear el instalador ejecutable de InstaFix
Genera un ejecutable standalone que incluye todas las dependencias
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """Verificar si PyInstaller está instalado"""
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
        return True
    except ImportError:
        print("❌ PyInstaller no encontrado")
        print("Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True

def clean_build_dirs():
    """Limpiar directorios de build anteriores"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Limpiado: {dir_name}")

def create_pyinstaller_spec(platform="macos"):
    """Crear archivo .spec para PyInstaller según la plataforma"""
    
    # Configuración específica por plataforma
    if platform == "windows":
        executable_name = 'InstaFix.exe'
        icon_path = 'assets/icon.ico' if os.path.exists('assets/icon.ico') else None
        console_mode = False
    else:  # macOS/Linux
        executable_name = 'InstaFix'
        icon_path = 'assets/icon.png' if os.path.exists('assets/icon.png') else None
        console_mode = False
    
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
        'sqlite3',
        'webbrowser',
        'urllib.parse',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'requests',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
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
    name='{executable_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={console_mode},
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{icon_path}' if {icon_path is not None} else None,
)
'''
    
    with open('InstaFix.spec', 'w') as f:
        f.write(spec_content)
    print("✅ Archivo InstaFix.spec creado")

def build_executable():
    """Construir el ejecutable usando PyInstaller"""
    print("🔨 Construyendo ejecutable...")
    
    # Ejecutar PyInstaller con el archivo .spec
    result = subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        'InstaFix.spec'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Ejecutable creado exitosamente")
        return True
    else:
        print("❌ Error al crear ejecutable:")
        print(result.stdout)
        print(result.stderr)
        return False

def create_installer_package():
    """Crear paquete de instalación con archivos adicionales"""
    package_dir = Path("InstaFix_Installer")
    
    # Crear directorio del instalador
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copiar ejecutable
    exe_source = Path("dist/InstaFix.exe" if sys.platform == "win32" else "dist/InstaFix")
    exe_dest = package_dir / exe_source.name
    
    if exe_source.exists():
        shutil.copy2(exe_source, exe_dest)
        print(f"✅ Ejecutable copiado a {exe_dest}")
    else:
        print("❌ No se encontró el ejecutable")
        return False
    
    # Copiar archivos de configuración
    config_files = ['.env.example', 'requirements.txt']
    for file in config_files:
        if os.path.exists(file):
            shutil.copy2(file, package_dir / file)
            print(f"✅ {file} copiado")
    
    # Crear README de instalación
    readme_content = """# InstaFix - Instalación

## Instrucciones de Instalación

1. **Ejecutar la aplicación:**
   - Ejecuta el archivo `InstaFix.exe` (Windows) o `InstaFix` (Mac/Linux)
   - La primera vez puede tardar un poco en iniciar

2. **Configuración inicial:**
   - Copia el archivo `.env.example` como `.env`
   - Edita el archivo `.env` con los datos de tu negocio:
     ```
     BUSINESS_NAME=Tu Nombre del Negocio
     BUSINESS_ADDRESS=Tu Dirección
     BUSINESS_PHONE=Tu Teléfono
     BUSINESS_MOBILE=Tu Celular
     BUSINESS_EMAIL=tu@email.com
     ```

3. **Primera ejecución:**
   - Al ejecutar por primera vez, se creará automáticamente la base de datos
   - La aplicación estará lista para usar

## Características

- ✅ Gestión completa de reparaciones
- ✅ Generación de PDFs profesionales
- ✅ Integración con WhatsApp Web
- ✅ Interface moderna y responsive
- ✅ Base de datos SQLite integrada
- ✅ Sin necesidad de instalar Python

## Soporte

Para soporte técnico o reportar problemas:
- GitHub: https://github.com/TomiRonco/InstaFix
- Email: soporte@instafix.com

## Versión

Versión: 1.0.0
Fecha: 2025-09-24
"""
    
    with open(package_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Paquete de instalación creado en:", package_dir.absolute())
    return True

def main():
    """Función principal del script de build"""
    print("🚀 InstaFix - Generador de Instalador")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('main.py'):
        print("❌ Error: Ejecuta este script desde el directorio raíz de InstaFix")
        sys.exit(1)
    
    try:
        # Paso 1: Verificar PyInstaller
        if not check_pyinstaller():
            print("❌ No se pudo instalar PyInstaller")
            sys.exit(1)
        
        # Paso 2: Limpiar builds anteriores
        clean_build_dirs()
        
        # Paso 3: Crear archivo .spec
        create_spec_file()
        
        # Paso 4: Construir ejecutable
        if not build_executable():
            print("❌ Falló la construcción del ejecutable")
            sys.exit(1)
        
        # Paso 5: Crear paquete de instalación
        if not create_installer_package():
            print("❌ Falló la creación del paquete")
            sys.exit(1)
        
        print("\n🎉 ¡Instalador creado exitosamente!")
        print(f"📁 Ubicación: {Path('InstaFix_Installer').absolute()}")
        print("\n📋 Próximos pasos:")
        print("1. Comprime la carpeta 'InstaFix_Installer'")
        print("2. Distribuye el archivo comprimido")
        print("3. Los usuarios solo necesitan extraer y ejecutar")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()