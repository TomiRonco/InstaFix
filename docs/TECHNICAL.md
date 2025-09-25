# Documentación Técnica - InstaFix

## Arquitectura del Sistema

### Estructura del Proyecto
```
InstaFix/
├── main.py                 # Punto de entrada principal
├── src/                    # Código fuente
│   ├── gui/               # Interfaz de usuario
│   │   ├── __init__.py
│   │   └── main_window.py # Ventana principal
│   ├── database/          # Manejo de base de datos
│   │   ├── __init__.py
│   │   └── manager.py     # Gestor de BD
│   └── whatsapp/          # Integración WhatsApp
│       ├── __init__.py
│       └── sender.py      # Envío de mensajes
├── assets/                # Recursos estáticos
├── scripts/               # Scripts de build
│   ├── build_installer.py    # Build macOS
│   ├── build_windows.py      # Build Windows
│   └── build_universal.py    # Build universal
├── docs/                  # Documentación
├── releases/              # Archivos de distribución
├── requirements.txt       # Dependencias Python
├── .env.example          # Plantilla configuración
├── .gitignore           # Archivos ignorados
├── LICENSE              # Licencia MIT
└── README.md            # Documentación principal
```

### Stack Tecnológico
- **Lenguaje**: Python 3.8+
- **GUI Framework**: tkinter + ttkbootstrap
- **Base de Datos**: SQLite3
- **PDF Generation**: ReportLab
- **HTTP Client**: requests
- **Image Processing**: Pillow (PIL)
- **Packaging**: PyInstaller

## Base de Datos

### Esquema SQLite
```sql
-- Tabla principal de reparaciones
CREATE TABLE reparaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_nombre TEXT NOT NULL,
    cliente_telefono TEXT NOT NULL,
    cliente_direccion TEXT,
    equipo_tipo TEXT NOT NULL,
    equipo_marca TEXT NOT NULL,
    equipo_modelo TEXT NOT NULL,
    equipo_serie TEXT,
    problema_descripcion TEXT NOT NULL,
    diagnostico TEXT,
    costo REAL NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para búsqueda eficiente
CREATE INDEX idx_cliente_nombre ON reparaciones(cliente_nombre);
CREATE INDEX idx_equipo_tipo ON reparaciones(equipo_tipo);
CREATE INDEX idx_fecha_creacion ON reparaciones(fecha_creacion);
```

### Operaciones CRUD
```python
# Crear reparación
def crear_reparacion(datos):
    query = """
    INSERT INTO reparaciones 
    (cliente_nombre, cliente_telefono, cliente_direccion,
     equipo_tipo, equipo_marca, equipo_modelo, equipo_serie,
     problema_descripcion, diagnostico, costo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
# Leer reparaciones
def obtener_reparaciones(filtro=None):
    query = "SELECT * FROM reparaciones"
    if filtro:
        query += f" WHERE cliente_nombre LIKE '%{filtro}%'"
    
# Actualizar reparación
def actualizar_reparacion(id, datos):
    query = """
    UPDATE reparaciones SET
    cliente_nombre=?, cliente_telefono=?, cliente_direccion=?,
    equipo_tipo=?, equipo_marca=?, equipo_modelo=?, equipo_serie=?,
    problema_descripcion=?, diagnostico=?, costo=?,
    fecha_actualizacion=CURRENT_TIMESTAMP
    WHERE id=?
    """
    
# Eliminar reparación
def eliminar_reparacion(id):
    query = "DELETE FROM reparaciones WHERE id=?"
```

## Interfaz de Usuario

### Arquitectura GUI
```python
# Patrón MVC implementado
class MainWindow:
    def __init__(self):
        self.root = ttk.Window(themename="superhero")
        self.db_manager = DatabaseManager()
        self.setup_gui()
        self.setup_bindings()
    
    def setup_gui(self):
        # Header
        self._crear_header()
        # Main content
        self._crear_contenido_principal()
        # Forms
        self._crear_formulario_reparacion()
        # List view
        self._crear_lista_reparaciones()
        # Actions
        self._crear_botones_accion()
```

### Componentes Principales
1. **Header**: Logo y datos del negocio
2. **Toolbar**: Botones de acción principal
3. **Form Panel**: Formulario de reparación
4. **List Panel**: Lista con filtros y búsqueda
5. **Status Bar**: Estado y mensajes

### Temas y Estilos
```python
# Temas disponibles
THEMES = {
    'light': ['cosmo', 'flatly', 'journal', 'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti'],
    'dark': ['darkly', 'cyborg', 'superhero', 'solar', 'vapor']
}

# Configuración de estilo personalizada
def aplicar_estilos_personalizados():
    style = ttk.Style()
    style.configure("Header.TLabel", font=("Arial", 16, "bold"))
    style.configure("Action.TButton", padding=(10, 5))
```

## Generación de PDF

### ReportLab Implementation
```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

class PDFGenerator:
    def __init__(self, business_config):
        self.business = business_config
        self.pagesize = A4
        self.width, self.height = A4
        
    def generar_comprobante(self, reparacion_data):
        # Configurar documento
        doc = SimpleDocTemplate(filename, pagesize=A4)
        
        # Elementos del documento
        story = []
        
        # Header con datos del negocio
        story.append(self._crear_header())
        
        # Datos del cliente y equipo
        story.append(self._crear_seccion_cliente(reparacion_data))
        
        # Detalles de reparación
        story.append(self._crear_seccion_reparacion(reparacion_data))
        
        # Condiciones y firma
        story.append(self._crear_seccion_condiciones())
        
        # Generar PDF
        doc.build(story)
```

### Layout del PDF
- **Página A4**: 210mm x 297mm
- **Márgenes**: 20mm todos los lados
- **Fuentes**: Helvetica para texto, Helvetica-Bold para títulos
- **Colores**: Negro para texto, gris para líneas

## Integración WhatsApp

### Funcionalidad
```python
class WhatsAppSender:
    def __init__(self):
        self.base_url = "https://web.whatsapp.com/send"
        
    def crear_mensaje(self, reparacion_data):
        template = """
        Hola {cliente}! 👋
        
        Te envío el presupuesto para la reparación de tu {equipo}:
        
        🔧 Problema: {problema}
        💰 Costo: ${costo}
        📅 Tiempo estimado: Según condiciones
        
        Cualquier consulta, no dudes en contactarme.
        
        {business_name}
        📞 {business_phone}
        """
        
        return template.format(**reparacion_data)
        
    def enviar_mensaje(self, telefono, mensaje):
        params = {
            'phone': self._formatear_telefono(telefono),
            'text': mensaje
        }
        url = f"{self.base_url}?{urlencode(params)}"
        webbrowser.open(url)
```

## Configuración

### Variables de Entorno
```python
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        
        # Información del negocio (requerido)
        self.BUSINESS_NAME = os.getenv('BUSINESS_NAME')
        self.BUSINESS_ADDRESS = os.getenv('BUSINESS_ADDRESS')
        self.BUSINESS_PHONE = os.getenv('BUSINESS_PHONE')
        self.BUSINESS_MOBILE = os.getenv('BUSINESS_MOBILE')
        self.BUSINESS_EMAIL = os.getenv('BUSINESS_EMAIL')
        
        # Configuración de la app (opcional)
        self.DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.THEME = os.getenv('THEME', 'superhero')
        self.DATABASE_PATH = os.getenv('DATABASE_PATH', './instafix.db')
        
        self.validate_config()
        
    def validate_config(self):
        required_fields = [
            'BUSINESS_NAME', 'BUSINESS_ADDRESS', 
            'BUSINESS_PHONE', 'BUSINESS_EMAIL'
        ]
        
        for field in required_fields:
            if not getattr(self, field):
                raise ValueError(f"Campo requerido faltante: {field}")
```

## Logging

### Sistema de Logs
```python
import logging
from datetime import datetime

def setup_logging(config):
    level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('instafix.log'),
            logging.StreamHandler() if config.DEBUG else logging.NullHandler()
        ]
    )
    
    logger = logging.getLogger('InstaFix')
    logger.info("Aplicación iniciada")
    return logger
```

## Testing

### Unit Tests
```python
import unittest
from src.database.manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager(':memory:')  # BD en memoria para tests
        
    def test_crear_reparacion(self):
        datos = {
            'cliente_nombre': 'Juan Pérez',
            'cliente_telefono': '+54911234567',
            'equipo_tipo': 'Smartphone',
            'costo': 25000
        }
        
        id_reparacion = self.db.crear_reparacion(datos)
        self.assertIsNotNone(id_reparacion)
        
    def test_buscar_reparaciones(self):
        # Crear datos de prueba
        self._crear_datos_prueba()
        
        # Buscar por nombre
        resultados = self.db.buscar_reparaciones('Juan')
        self.assertEqual(len(resultados), 1)
```

### Integration Tests
```python
class TestPDFGeneration(unittest.TestCase):
    def test_generar_pdf_completo(self):
        generator = PDFGenerator(config)
        datos_reparacion = self._obtener_datos_prueba()
        
        filename = generator.generar_comprobante(datos_reparacion)
        
        self.assertTrue(os.path.exists(filename))
        self.assertGreater(os.path.getsize(filename), 1000)  # PDF no vacío
```

## Build y Distribución

### PyInstaller Configuration
```python
# build_config.py
PYINSTALLER_OPTIONS = {
    'name': 'InstaFix',
    'onefile': True,
    'windowed': True,
    'icon': 'assets/icon.ico',
    'add_data': [
        ('assets', 'assets'),
        ('.env.example', '.'),
        ('requirements.txt', '.')
    ],
    'hidden_imports': [
        'tkinter', 'ttkbootstrap', 'reportlab',
        'sqlite3', 'requests', 'PIL'
    ],
    'exclude_modules': ['matplotlib', 'numpy', 'pandas'],
    'optimize': 2
}
```

### Build Process
1. **Preparación**: Limpiar archivos temporales
2. **Validación**: Verificar dependencias
3. **Compilación**: PyInstaller con configuración específica
4. **Empaquetado**: Crear carpeta instalador con archivos adicionales
5. **Compresión**: Generar ZIP para distribución

## Performance

### Optimizaciones
- **Lazy Loading**: Cargar datos bajo demanda
- **Índices BD**: Para búsquedas eficientes
- **Cache**: Datos de configuración en memoria
- **Threading**: Operaciones IO en hilos separados

### Memory Management
- **Conexiones BD**: Pool de conexiones reutilizables
- **Images**: Redimensionamiento automático
- **PDF**: Generación streaming para archivos grandes

## Seguridad

### Validación de Datos
```python
def validar_telefono(telefono):
    pattern = r'^\+?[\d\s\-\(\)]{10,15}$'
    return re.match(pattern, telefono) is not None

def sanitizar_entrada(texto):
    # Remover caracteres peligrosos
    return re.sub(r'[<>"\';]', '', texto)
```

### Manejo de Errores
```python
class InstaFixError(Exception):
    """Excepción base para InstaFix"""
    pass

class DatabaseError(InstaFixError):
    """Errores de base de datos"""
    pass

class ValidationError(InstaFixError):
    """Errores de validación"""
    pass

def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error en {func.__name__}: {e}")
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
    return wrapper
```

## API Reference

### DatabaseManager
```python
class DatabaseManager:
    def __init__(self, db_path: str)
    def crear_reparacion(self, datos: dict) -> int
    def obtener_reparacion(self, id: int) -> dict
    def actualizar_reparacion(self, id: int, datos: dict) -> bool
    def eliminar_reparacion(self, id: int) -> bool
    def buscar_reparaciones(self, query: str) -> list
    def obtener_todas_reparaciones(self) -> list
```

### PDFGenerator
```python
class PDFGenerator:
    def __init__(self, config: Config)
    def generar_comprobante(self, datos: dict) -> str
    def validar_datos(self, datos: dict) -> bool
```

### WhatsAppSender
```python
class WhatsAppSender:
    def crear_mensaje(self, datos: dict) -> str
    def enviar_mensaje(self, telefono: str, mensaje: str) -> bool
    def formatear_telefono(self, telefono: str) -> str
```

## Contribución

### Code Style
- **PEP 8**: Guía de estilo estándar
- **Type Hints**: Para funciones públicas
- **Docstrings**: Formato Google style
- **Comments**: En español, explicativos

### Workflow
1. **Fork** del repositorio
2. **Branch** para nueva feature
3. **Develop** con tests
4. **Test** local completo
5. **Pull Request** con descripción detallada

### Testing Requirements
- **Unit Tests**: >80% coverage
- **Integration Tests**: Principales workflows
- **Manual Testing**: En ambas plataformas