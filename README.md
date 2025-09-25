# 🔧 InstaFix - Sistema de Gestión de Reparaciones

**InstaFix** es una aplicación de escritorio desarrollada en Python para gestionar reparaciones de equipos electrónicos de manera profesional. Incluye generación de PDFs, integración con WhatsApp y una interfaz moderna.

## 🚀 Características Principales

### ✨ Gestión de Reparaciones
- **Registro completo de reparaciones** con datos del cliente y equipo
- **Base de datos SQLite** integrada para almacenamiento local
- **Interfaz moderna** con temas personalizables usando ttkbootstrap
- **Búsqueda y filtrado** de reparaciones existentes

### 📄 Generación de Documentos
- **PDFs profesionales** con diseño limpio y datos consolidados
- **Comprobantes de reparación** con información del negocio
- **Layout optimizado** sin espacios en blanco para completar
- **Condiciones de servicio** integradas en el documento

### 📱 Integración WhatsApp
- **Envío automático** de presupuestos vía WhatsApp Web
- **Mensajes personalizados** con datos del cliente y reparación
- **Apertura directa** del chat en el navegador

### 🎨 Interfaz de Usuario
- **Diseño responsive** que se adapta al tamaño de ventana
- **Temas modernos** con colores profesionales
- **Navegación intuitiva** con formularios bien organizados
- **Compatible** con Windows 10/11 y macOS 10.15+

## 📦 Instalación

### Opción 1: Ejecutables Precompilados (Recomendado)

#### Para Windows:
1. Descarga `InstaFix_v1.0.0_Windows.zip` desde [Releases](releases/)
2. Extrae el contenido en una carpeta (ej: `C:\InstaFix\`)
3. Copia `.env.example` como `.env` y configura tus datos del negocio
4. Ejecuta `InstaFix.exe` o `Ejecutar_InstaFix.bat`

#### Para macOS:
1. Descarga `InstaFix_v1.0.0_macOS.zip` desde [Releases](releases/)
2. Extrae el contenido en una carpeta (ej: `/Applications/InstaFix/`)
3. Copia `.env.example` como `.env` y configura tus datos del negocio
4. Ejecuta `InstaFix` (puede requerir autorización en Seguridad)

### Opción 2: Instalación desde Código Fuente

#### Requisitos:
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

#### Pasos:
```bash
# Clonar repositorio
git clone https://github.com/TomiRonco/InstaFix.git
cd InstaFix

# Crear entorno virtual (recomendado)
python -m venv .venv

# Activar entorno virtual
# En Windows:
.venv\Scripts\activate
# En macOS/Linux:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con los datos de tu negocio

# Ejecutar aplicación
python main.py
```

## ⚙️ Configuración

### Archivo `.env`
Crea un archivo `.env` basado en `.env.example` con tus datos:

```bash
# Información del Negocio
BUSINESS_NAME=Tu Nombre del Negocio
BUSINESS_ADDRESS=Tu Dirección Completa, Ciudad, CP
BUSINESS_PHONE=+54 11 1234-5678
BUSINESS_MOBILE=+54 9 11 1234-5678
BUSINESS_EMAIL=tu@email.com

# Configuración de la Aplicación (Opcional)
DEBUG=False
LOG_LEVEL=INFO
```

### Primera Ejecución
Al ejecutar la aplicación por primera vez:
1. Se creará automáticamente la base de datos `instafix.db`
2. Se inicializará el sistema de logging
3. Se configurará la interfaz con tus datos del negocio

## 📖 Uso de la Aplicación

### 1. Pantalla Principal
- **Botón "Nueva Reparación"**: Abrir formulario para registrar nueva reparación
- **Lista de reparaciones**: Ver reparaciones existentes con búsqueda y filtros
- **Botones de acción**: Editar, eliminar, generar PDF, enviar WhatsApp

### 2. Formulario de Reparación
- **Datos del Cliente**: Nombre, teléfono, dirección
- **Información del Equipo**: Tipo, marca, modelo, número de serie
- **Detalles de la Reparación**: Descripción del problema, diagnóstico, costo
- **Validación automática**: Campos requeridos y formatos correctos

### 3. Generación de PDF
- **Diseño profesional**: Header con datos del negocio
- **Información consolidada**: Cliente y equipo en una sección
- **Detalles de reparación**: Descripción, costo y condiciones
- **Guardado automático**: PDF se guarda en carpeta del proyecto

### 4. WhatsApp Integration
- **Mensaje personalizado**: Se genera automáticamente con datos del cliente
- **Apertura automática**: Se abre WhatsApp Web con el mensaje preparado
- **Información incluida**: Nombre, equipo, costo y datos de contacto

## 🛠️ Desarrollo y Build

### Estructura del Proyecto
```
InstaFix/
├── src/                    # Código fuente
│   ├── gui/               # Interfaz de usuario
│   ├── database/          # Manejo de base de datos
│   └── whatsapp/          # Integración WhatsApp
├── assets/                # Recursos (iconos, imágenes)
├── scripts/               # Scripts de build y deploy
├── docs/                  # Documentación
├── releases/              # Archivos de distribución
├── main.py               # Punto de entrada
├── requirements.txt      # Dependencias Python
├── .env.example         # Plantilla de configuración
└── README.md            # Este archivo
```

### Generar Ejecutables

#### Para ambas plataformas:
```bash
cd scripts
python build_universal.py
```

#### Solo Windows:
```bash
cd scripts
python build_windows.py
```

#### Solo macOS:
```bash
cd scripts
python build_installer.py
```

### Dependencias Principales
- **tkinter**: Interfaz gráfica nativa
- **ttkbootstrap**: Temas modernos para tkinter
- **reportlab**: Generación de PDFs
- **sqlite3**: Base de datos (incluido en Python)
- **requests**: Cliente HTTP para funcionalidades web
- **Pillow**: Manejo de imágenes
- **PyInstaller**: Generación de ejecutables

## 🧪 Testing y Calidad

### Ejecutar Pruebas
```bash
# Prueba de la aplicación principal
python main.py

# Verificar dependencias
pip check

# Validar sintaxis
python -m py_compile main.py src/**/*.py
```

### Logs y Debugging
- Los logs se guardan en `instafix.log`
- Nivel de logging configurable en `.env`
- Información de errores detallada para debugging

## 📋 Requisitos del Sistema

### Mínimos:
- **Windows**: Windows 10 (1903) o superior
- **macOS**: macOS 10.15 (Catalina) o superior
- **RAM**: 512 MB disponible
- **Almacenamiento**: 100 MB espacio libre
- **Resolución**: 1024x768 mínimo

### Recomendados:
- **Windows**: Windows 11
- **macOS**: macOS 12.0 (Monterey) o superior
- **RAM**: 1 GB disponible
- **Almacenamiento**: 500 MB espacio libre
- **Resolución**: 1920x1080 o superior

## 🔧 Solución de Problemas

### Windows
**Problema**: "Windows protegió tu PC"
- **Solución**: Hacer clic en "Más información" → "Ejecutar de todas formas"
- **Causa**: Ejecutables de PyInstaller pueden activar SmartScreen

**Problema**: Antivirus bloquea la aplicación
- **Solución**: Agregar InstaFix.exe a las excepciones del antivirus
- **Causa**: Falso positivo común en ejecutables empaquetados

### macOS
**Problema**: "La aplicación no se puede abrir"
- **Solución**: Clic derecho → "Abrir" → "Abrir"
- **Alternativa**: Sistema → Seguridad y Privacidad → "Abrir de todas formas"

**Problema**: Aplicación muy lenta al iniciar
- **Solución**: Normal en primera ejecución, siguientes serán más rápidas

### General
**Problema**: Base de datos no se crea
- **Solución**: Verificar permisos de escritura en la carpeta del programa

**Problema**: PDF no se genera
- **Solución**: Verificar que el archivo `.env` esté configurado correctamente

## 🤝 Contribución

### Cómo Contribuir
1. Fork del repositorio
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Estándares de Código
- **PEP 8**: Seguir guía de estilo de Python
- **Documentación**: Docstrings para todas las funciones
- **Testing**: Incluir pruebas para nuevas funcionalidades
- **Commits**: Mensajes descriptivos en español

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte y Contacto

- **GitHub Issues**: [Reportar problemas](https://github.com/TomiRonco/InstaFix/issues)
- **Email**: soporte@instafix.com
- **Documentación**: [Wiki del proyecto](https://github.com/TomiRonco/InstaFix/wiki)

## 🎉 Changelog

### v1.0.0 (24 de septiembre de 2025)
- ✅ **Lanzamiento inicial**
- ✅ **Gestión completa de reparaciones**
- ✅ **Generación de PDFs profesionales**
- ✅ **Integración con WhatsApp**
- ✅ **Ejecutables para Windows y macOS**
- ✅ **Interface moderna con ttkbootstrap**
- ✅ **Base de datos SQLite integrada**

---

**InstaFix** - *Simplificando la gestión de reparaciones*

Desarrollado con ❤️ por [TomiRonco](https://github.com/TomiRonco)