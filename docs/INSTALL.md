# Guía de Instalación Detallada - InstaFix

## Instalación Ejecutables (Sin Python)

### Windows

#### Requisitos Previos
- Windows 10 versión 1903 o superior
- 100 MB de espacio libre en disco
- Conexión a internet para WhatsApp (opcional)

#### Proceso de Instalación

1. **Descarga**
   - Descarga `InstaFix_v1.0.0_Windows.zip` desde la carpeta `releases/`
   - Tamaño aproximado: 19 MB

2. **Extracción**
   ```
   Ubicación recomendada: C:\Program Files\InstaFix\
   O cualquier carpeta de tu elección
   ```

3. **Configuración**
   - Navega a la carpeta extraída
   - Busca el archivo `.env.example`
   - Copia y renombra como `.env`
   - Abre `.env` con Bloc de notas
   - Completa con tus datos:
   ```
   BUSINESS_NAME=Servicio Técnico Juan Pérez
   BUSINESS_ADDRESS=Av. Corrientes 1234, Buenos Aires, CP 1043
   BUSINESS_PHONE=+54 11 4567-8901
   BUSINESS_MOBILE=+54 9 11 2345-6789
   BUSINESS_EMAIL=contacto@serviciotecnico.com
   ```

4. **Primera Ejecución**
   - Doble clic en `InstaFix.exe`
   - Si aparece "Windows protegió tu PC":
     - Clic en "Más información"
     - Clic en "Ejecutar de todas formas"
   - Esperar 30-60 segundos (primera vez)
   - Se creará automáticamente `instafix.db`

5. **Acceso Rápido** (Opcional)
   - Clic derecho en `InstaFix.exe`
   - "Crear acceso directo"
   - Mover acceso directo al Escritorio

#### Solución de Problemas Windows

**Error: "No se puede ejecutar"**
- Verificar que tienes permisos de administrador
- Clic derecho → "Ejecutar como administrador"

**Error: Antivirus bloquea el archivo**
- Agregar carpeta InstaFix a excepciones del antivirus
- Deshabilitar temporalmente el análisis en tiempo real

**Error: "Falta archivo DLL"**
- Descargar e instalar Microsoft Visual C++ Redistributable
- Reiniciar el sistema

### macOS

#### Requisitos Previos
- macOS 10.15 (Catalina) o superior
- 100 MB de espacio libre en disco
- Permisos para ejecutar aplicaciones de desarrolladores no identificados

#### Proceso de Instalación

1. **Descarga**
   - Descarga `InstaFix_v1.0.0_macOS.zip` desde la carpeta `releases/`
   - Tamaño aproximado: 16 MB

2. **Extracción**
   ```
   Ubicación recomendada: /Applications/InstaFix/
   O carpeta personal: ~/InstaFix/
   ```

3. **Configuración**
   - Abre Terminal y navega a la carpeta:
   ```bash
   cd /Applications/InstaFix/
   cp .env.example .env
   nano .env
   ```
   - O usar Finder y TextEdit para editar `.env`

4. **Autorización de Seguridad**
   - Primera ejecución: doble clic en `InstaFix`
   - Aparecerá: "InstaFix no se puede abrir"
   - Ir a: Preferencias del Sistema → Seguridad y Privacidad
   - Clic en "Abrir de todas formas"
   - Confirmar en el diálogo

5. **Ejecución Normal**
   - Siguientes ejecuciones: doble clic normal
   - Agregar al Dock para acceso rápido

#### Solución de Problemas macOS

**Error: "App dañada"**
- Ejecutar en Terminal:
```bash
sudo xattr -cr /path/to/InstaFix
```

**Error: Muy lento al iniciar**
- Normal en primera ejecución
- Siguientes inicios serán más rápidos

## Instalación desde Código Fuente

### Requisitos del Sistema
- Python 3.8 o superior
- pip 20.0 o superior
- Git (para clonar repositorio)

### Instalación Paso a Paso

#### 1. Obtener el Código
```bash
# Opción A: Clonar repositorio
git clone https://github.com/TomiRonco/InstaFix.git
cd InstaFix

# Opción B: Descargar ZIP y extraer
# Descargar desde GitHub → Code → Download ZIP
```

#### 2. Configurar Entorno Virtual
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Verificar activación
which python  # Debe mostrar ruta del .venv
```

#### 3. Instalar Dependencias
```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

#### 4. Configuración
```bash
# Crear archivo de configuración
cp .env.example .env

# Editar configuración
# Windows: notepad .env
# macOS: nano .env
# Linux: nano .env
```

#### 5. Primera Ejecución
```bash
# Ejecutar aplicación
python main.py

# Si hay errores, verificar dependencias
pip check
```

### Dependencias Detalladas

```
tkinter>=8.6        # Interfaz gráfica (incluido en Python)
ttkbootstrap>=1.10  # Temas modernos
reportlab>=3.6      # Generación PDFs
sqlite3             # Base de datos (incluido en Python)
requests>=2.31      # Cliente HTTP
Pillow>=10.0        # Manejo de imágenes
webbrowser          # Apertura navegador (incluido)
urllib3>=2.0        # Utilidades URL (incluido)
pathlib             # Manejo rutas (incluido)
logging             # Sistema de logs (incluido)
datetime            # Fechas y horas (incluido)
json                # Manejo JSON (incluido)
os                  # Sistema operativo (incluido)
sys                 # Sistema Python (incluido)
```

### Generar Ejecutables Propios

#### Instalar PyInstaller
```bash
pip install pyinstaller>=5.13.0
```

#### Para Windows
```bash
cd scripts
python build_windows.py
```

#### Para macOS
```bash
cd scripts
python build_installer.py
```

#### Para Ambos
```bash
cd scripts
python build_universal.py
```

## Verificación de Instalación

### Tests Básicos
```bash
# Verificar Python
python --version

# Verificar pip
pip --version

# Verificar dependencias
pip check

# Test de importación
python -c "import tkinter; print('tkinter OK')"
python -c "import ttkbootstrap; print('ttkbootstrap OK')"
python -c "import reportlab; print('reportlab OK')"
```

### Test de Funcionalidad
```bash
# Ejecutar aplicación en modo test
python main.py --test

# Verificar creación de BD
ls -la instafix.db

# Verificar logs
cat instafix.log
```

## Configuración Avanzada

### Variables de Entorno Completas
```bash
# Información del Negocio (REQUERIDO)
BUSINESS_NAME=Tu Servicio Técnico
BUSINESS_ADDRESS=Dirección Completa con CP
BUSINESS_PHONE=+54 11 1234-5678
BUSINESS_MOBILE=+54 9 11 1234-5678
BUSINESS_EMAIL=contacto@empresa.com

# Configuración de la App (OPCIONAL)
DEBUG=False
LOG_LEVEL=INFO
DATABASE_PATH=./instafix.db
PDF_OUTPUT_DIR=./pdfs/

# Configuración WhatsApp (OPCIONAL)
WHATSAPP_ENABLED=True
WHATSAPP_MESSAGE_TEMPLATE=custom

# Configuración UI (OPCIONAL)
THEME=superhero
WINDOW_SIZE=1200x800
WINDOW_RESIZABLE=True
```

### Personalización de Temas
```python
# Temas disponibles en ttkbootstrap:
THEMES = [
    'cosmo', 'flatly', 'journal', 'literal',
    'lumen', 'minty', 'pulse', 'sandstone',
    'united', 'yeti', 'morph', 'simplex',
    'cerculean', 'solar', 'superhero', 'darkly',
    'cyborg', 'vapor'
]
```

## Troubleshooting Avanzado

### Logs y Debugging
```bash
# Habilitar modo debug
echo "DEBUG=True" >> .env
echo "LOG_LEVEL=DEBUG" >> .env

# Ver logs en tiempo real
tail -f instafix.log

# Limpiar logs
> instafix.log
```

### Problemas de Base de Datos
```bash
# Verificar integridad de BD
sqlite3 instafix.db ".schema"
sqlite3 instafix.db "PRAGMA integrity_check;"

# Backup de BD
cp instafix.db instafix_backup_$(date +%Y%m%d).db

# Recrear BD (CUIDADO: borra datos)
rm instafix.db
python main.py  # Se recreará automáticamente
```

### Problemas de PDF
```bash
# Verificar ReportLab
python -c "from reportlab.pdfgen import canvas; print('PDF OK')"

# Test de generación PDF
python -c "
from reportlab.pdfgen import canvas
c = canvas.Canvas('test.pdf')
c.drawString(100, 750, 'Test PDF')
c.save()
print('test.pdf creado')
"
```

### Reinstalación Limpia
```bash
# Limpiar entorno virtual
rm -rf .venv

# Limpiar archivos compilados
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete

# Reinstalar desde cero
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r requirements.txt
```