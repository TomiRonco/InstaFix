#!/usr/bin/env python3
"""
InstaFix - Build Script Universal
Genera ejecutables para distribución en macOS y Windows
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import platform
from datetime import datetime

def print_header():
    """Mostrar encabezado del script"""
    print("🚀 InstaFix - Generador de Instaladores Universal")
    print("=" * 55)
    print(f"🖥️  Sistema actual: {platform.system()}")
    print()

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

def create_spec_for_platform(target_platform):
    """Crear archivo .spec específico para cada plataforma"""
    
    if target_platform == "windows":
        executable_name = 'InstaFix.exe'
        icon_path = 'assets/icon.ico' if os.path.exists('assets/icon.ico') else None
        spec_name = 'InstaFix_Windows.spec'
        console_mode = False
    else:  # macOS
        executable_name = 'InstaFix'
        icon_path = 'assets/icon.png' if os.path.exists('assets/icon.png') else None
        spec_name = 'InstaFix_macOS.spec'
        console_mode = False
    
    spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-
# Generated for {target_platform.upper()}

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
    
    with open(spec_name, 'w') as f:
        f.write(spec_content)
    print(f"✅ Archivo {spec_name} creado")
    return spec_name

def build_executable(spec_file):
    """Construir el ejecutable usando PyInstaller"""
    print(f"🔨 Construyendo ejecutable con {spec_file}...")
    
    # Ejecutar PyInstaller con el archivo .spec
    result = subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        spec_file
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Ejecutable creado exitosamente")
        return True
    else:
        print("❌ Error al crear ejecutable:")
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return False

def create_readme(platform, installer_dir):
    """Crear README específico para cada plataforma"""
    
    if platform == "windows":
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
   - Doble clic en `InstaFix.exe` o usar `Ejecutar_InstaFix.bat`
   - La primera vez puede tardar un poco en iniciar (30-60 segundos)
   - Se creará automáticamente la base de datos

4. **Crear acceso directo (Opcional):**
   - Clic derecho en `InstaFix.exe` → "Crear acceso directo"
   - Mueve el acceso directo al Escritorio o al menú Inicio

## Solución de Problemas

### Si no abre la aplicación:
1. Asegúrate que Windows no esté bloqueando el archivo
2. Clic derecho en InstaFix.exe → "Propiedades" → "Desbloquear" (si aparece)
3. Ejecuta como Administrador (clic derecho → "Ejecutar como administrador")

### Si aparece error de antivirus:
- Agrega la carpeta de InstaFix a las excepciones de tu antivirus
- Es normal que algunos antivirus marquen ejecutables de PyInstaller como sospechosos

## Características

- ✅ Gestión completa de reparaciones
- ✅ Generación de PDFs profesionales
- ✅ Integración con WhatsApp Web
- ✅ Interface moderna y responsive
- ✅ Base de datos SQLite integrada
- ✅ Sin necesidad de instalar Python
- ✅ Compatible con Windows 10/11

## Soporte

Para soporte técnico o reportar problemas:
- GitHub: https://github.com/TomiRonco/InstaFix
- Email: soporte@instafix.com

## Versión

Versión: 1.0.0 Windows Edition
Fecha: 24 de septiembre de 2025
Plataforma: Windows x64
"""
        readme_filename = "README_Windows.md"
        
        # Crear archivo batch para facilitar la ejecución
        bat_content = '''@echo off
echo Iniciando InstaFix...
echo Por favor espera, puede tardar un momento en cargar...
start "" "InstaFix.exe"
'''
        
        bat_path = installer_dir / "Ejecutar_InstaFix.bat"
        with open(bat_path, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        print("✅ Ejecutar_InstaFix.bat creado")
        
    else:  # macOS
        readme_content = """# InstaFix - Instalación para macOS

## Instrucciones de Instalación

### Requisitos del Sistema
- macOS 10.15 (Catalina) o superior
- No requiere Python instalado

### Pasos de Instalación

1. **Extraer archivos:**
   - Extrae todos los archivos del ZIP en una carpeta de tu elección
   - Recomendado: `/Applications/InstaFix/` o carpeta personal

2. **Configuración inicial:**
   - Copia el archivo `.env.example` como `.env`
   - Abre `.env` con TextEdit o tu editor preferido
   - Edita el archivo con los datos de tu negocio:
     ```
     BUSINESS_NAME=Tu Nombre del Negocio
     BUSINESS_ADDRESS=Tu Dirección Completa
     BUSINESS_PHONE=Tu Teléfono Fijo
     BUSINESS_MOBILE=Tu Celular
     BUSINESS_EMAIL=tu@email.com
     ```
   - Guarda el archivo

3. **Ejecutar la aplicación:**
   - Doble clic en `InstaFix`
   - Si aparece advertencia de seguridad: Sistema → Seguridad → "Abrir de todos modos"
   - La primera vez puede tardar un poco en iniciar (30-60 segundos)
   - Se creará automáticamente la base de datos

4. **Agregar al Dock (Opcional):**
   - Arrastra `InstaFix` al Dock para acceso rápido

## Solución de Problemas

### Si macOS bloquea la aplicación:
1. Clic derecho en InstaFix → "Abrir"
2. O ir a: Sistema → Seguridad y Privacidad → "Abrir de todos modos"
3. Una vez autorizado, funcionará con doble clic normal

## Características

- ✅ Gestión completa de reparaciones
- ✅ Generación de PDFs profesionales
- ✅ Integración con WhatsApp Web
- ✅ Interface moderna y responsive
- ✅ Base de datos SQLite integrada
- ✅ Sin necesidad de instalar Python
- ✅ Compatible con macOS 10.15+

## Soporte

Para soporte técnico o reportar problemas:
- GitHub: https://github.com/TomiRonco/InstaFix
- Email: soporte@instafix.com

## Versión

Versión: 1.0.0 macOS Edition
Fecha: 24 de septiembre de 2025
Plataforma: macOS Universal
"""
        readme_filename = "README_macOS.md"
    
    # Escribir archivo README
    readme_path = installer_dir / readme_filename
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✅ {readme_filename} creado")

def create_installer_package(platform):
    """Crear paquete de instalación para la plataforma específica"""
    
    if platform == "windows":
        package_dir = Path("InstaFix_Installer_Windows")
        executable_name = "InstaFix.exe"
    else:  # macOS
        package_dir = Path("InstaFix_Installer_macOS")
        executable_name = "InstaFix"
    
    # Crear directorio del instalador
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copiar ejecutable
    exe_source = Path(f"dist/{executable_name}")
    exe_dest = package_dir / executable_name
    
    if exe_source.exists():
        shutil.copy2(exe_source, exe_dest)
        print(f"✅ Ejecutable copiado a {exe_dest}")
    else:
        print(f"❌ No se encontró el ejecutable {executable_name}")
        return False
    
    # Copiar archivos de configuración
    config_files = ['.env.example', 'requirements.txt']
    for file in config_files:
        if os.path.exists(file):
            shutil.copy2(file, package_dir / file)
            print(f"✅ {file} copiado")
    
    # Crear README específico para la plataforma
    create_readme(platform, package_dir)
    
    print(f"✅ Paquete de instalación {platform} creado en: {package_dir.absolute()}")
    return package_dir

def create_zip_package(installer_dir, platform):
    """Crear archivo ZIP para distribución"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d")
        zip_name = f"InstaFix_v1.0.0_{platform.title()}_{timestamp}.zip"
        
        # Comprimir usando shutil
        base_name = zip_name.replace('.zip', '')
        shutil.make_archive(base_name, 'zip', str(installer_dir))
        
        print(f"✅ Archivo ZIP creado: {zip_name}")
        
        # Mostrar tamaño del archivo
        if os.path.exists(zip_name):
            size_mb = os.path.getsize(zip_name) / (1024 * 1024)
            print(f"📦 Tamaño: {size_mb:.1f} MB")
        
        return zip_name
        
    except Exception as e:
        print(f"❌ Error creando ZIP: {e}")
        return None

def cleanup():
    """Limpiar archivos temporales"""
    try:
        # Limpiar archivos de build
        temp_dirs = ['build', '__pycache__']
        for dir_name in temp_dirs:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
        
        # Limpiar archivos .spec temporales
        spec_files = ['InstaFix_Windows.spec', 'InstaFix_macOS.spec']
        for spec_file in spec_files:
            if os.path.exists(spec_file):
                os.remove(spec_file)
        
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
        
        # Preguntar qué plataforma(s) generar
        print("🎯 Selecciona las plataformas a generar:")
        print("1. Solo Windows")
        print("2. Solo macOS")
        print("3. Ambas plataformas")
        
        choice = input("\\nElige una opción (1-3): ").strip()
        
        platforms = []
        if choice == "1":
            platforms = ["windows"]
        elif choice == "2":
            platforms = ["macos"]
        elif choice == "3":
            platforms = ["windows", "macos"]
        else:
            print("❌ Opción inválida")
            return False
        
        print()
        generated_files = []
        
        # Generar para cada plataforma seleccionada
        for platform in platforms:
            print(f"🏗️  Generando instalador para {platform.upper()}...")
            print("-" * 40)
            
            # Crear archivo .spec
            spec_file = create_spec_for_platform(platform)
            
            # Construir ejecutable
            if not build_executable(spec_file):
                print(f"❌ Error generando ejecutable para {platform}")
                continue
            
            # Crear paquete de instalación
            installer_dir = create_installer_package(platform)
            if not installer_dir:
                print(f"❌ Error creando paquete para {platform}")
                continue
            
            # Crear ZIP para distribución
            zip_file = create_zip_package(installer_dir, platform)
            if zip_file:
                generated_files.append(zip_file)
            
            print(f"✅ Instalador para {platform.upper()} completado\\n")
        
        # Limpiar archivos temporales
        cleanup()
        
        # Resumen final
        print("🎉 ¡Proceso completado exitosamente!")
        print("=" * 50)
        print("📦 Archivos generados:")
        for file in generated_files:
            size_mb = os.path.getsize(file) / (1024 * 1024)
            print(f"   • {file} ({size_mb:.1f} MB)")
        
        print("\\n📋 Instrucciones de distribución:")
        print("1. Comparte los archivos ZIP generados")
        print("2. Los usuarios deben seguir el README correspondiente")
        print("3. No requieren Python instalado")
        
        return True
        
    except KeyboardInterrupt:
        print("\\n⏹️  Proceso cancelado por el usuario")
        return False
    except Exception as e:
        print(f"\\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)