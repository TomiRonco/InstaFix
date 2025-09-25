# Guía de Usuario - InstaFix

## Introducción

InstaFix es un sistema completo para gestionar reparaciones de equipos electrónicos. Esta guía te ayudará a usar todas las funcionalidades de la aplicación.

## Interfaz Principal

### Pantalla de Inicio
Al abrir InstaFix verás:
- **Barra superior**: Logo y nombre de tu negocio
- **Botón "Nueva Reparación"**: Para registrar una nueva reparación
- **Lista de reparaciones**: Tabla con todas las reparaciones registradas
- **Barra de búsqueda**: Para filtrar reparaciones
- **Botones de acción**: Editar, eliminar, PDF, WhatsApp

## Crear Nueva Reparación

### Datos del Cliente
1. **Nombre completo**: Nombre y apellido del cliente
2. **Teléfono**: Número de contacto (formato: +54 9 11 1234-5678)
3. **Dirección**: Dirección completa del cliente

### Información del Equipo
1. **Tipo de equipo**: Seleccionar de la lista desplegable
   - Smartphone
   - Tablet
   - Laptop
   - PC de Escritorio
   - Consola de Videojuegos
   - Otro
2. **Marca**: Marca del equipo
3. **Modelo**: Modelo específico
4. **Número de serie**: Serial del equipo (opcional)

### Detalles de la Reparación
1. **Descripción del problema**: Detalle de la falla reportada
2. **Diagnóstico**: Tu diagnóstico técnico
3. **Costo de reparación**: Precio en formato numérico (ej: 25000)

### Guardar Reparación
- Clic en **"Guardar Reparación"**
- Todos los campos marcados con * son obligatorios
- La aplicación validará los datos antes de guardar

## Gestionar Reparaciones Existentes

### Ver Lista de Reparaciones
La tabla muestra:
- **ID**: Número único de la reparación
- **Cliente**: Nombre del cliente
- **Equipo**: Tipo y modelo del equipo
- **Problema**: Descripción breve del problema
- **Costo**: Precio de la reparación
- **Fecha**: Fecha de registro

### Buscar y Filtrar
1. **Barra de búsqueda**: Escribe cualquier término
   - Busca en nombre del cliente
   - Busca en tipo de equipo
   - Busca en descripción del problema
2. **Filtrado automático**: Los resultados se actualizan mientras escribes

### Acciones sobre Reparaciones

#### Editar Reparación
1. Selecciona una reparación de la lista
2. Clic en **"Editar"**
3. Modifica los datos necesarios
4. Clic en **"Actualizar Reparación"**

#### Eliminar Reparación
1. Selecciona una reparación de la lista
2. Clic en **"Eliminar"**
3. Confirma la eliminación en el diálogo
4. ⚠️ **Advertencia**: Esta acción no se puede deshacer

## Generar PDF

### Crear Comprobante
1. Selecciona una reparación de la lista
2. Clic en **"Generar PDF"**
3. El PDF se crea automáticamente
4. Se guarda en la carpeta del programa

### Contenido del PDF
El comprobante incluye:
- **Header**: Datos de tu negocio
- **Información del cliente**: Nombre, teléfono, dirección
- **Datos del equipo**: Tipo, marca, modelo, serie
- **Detalles de reparación**: Descripción y costo
- **Condiciones**: Términos del servicio
- **Línea de firma**: Espacio para firma del cliente

### Ubicación del PDF
- Se guarda con nombre: `Comprobante_[Cliente]_[Fecha].pdf`
- Ubicación: Carpeta donde está instalado InstaFix
- Se abre automáticamente después de crear

## Integración WhatsApp

### Enviar Presupuesto
1. Selecciona una reparación de la lista
2. Clic en **"Enviar WhatsApp"**
3. Se abre WhatsApp Web en tu navegador
4. El mensaje se genera automáticamente

### Contenido del Mensaje
```
Hola [Nombre del Cliente]! 👋

Te envío el presupuesto para la reparación de tu [Equipo]:

🔧 Problema: [Descripción]
💰 Costo: $[Precio]
📅 Tiempo estimado: Según condiciones

Cualquier consulta, no dudes en contactarme.

[Tu Nombre de Negocio]
📞 [Tu Teléfono]
```

### Usar WhatsApp
1. **Primera vez**: WhatsApp Web pedirá escanear código QR con tu teléfono
2. **Siguientes veces**: Se conecta automáticamente
3. **Enviar mensaje**: El mensaje está preparado, solo clic en enviar
4. **Personalizar**: Puedes modificar el mensaje antes de enviar

## Configuración

### Datos del Negocio
Para cambiar los datos de tu negocio:
1. Cierra InstaFix
2. Abre el archivo `.env` con un editor de texto
3. Modifica los valores:
```
BUSINESS_NAME=Tu Nuevo Nombre
BUSINESS_ADDRESS=Tu Nueva Dirección
BUSINESS_PHONE=Tu Nuevo Teléfono
BUSINESS_MOBILE=Tu Nuevo Celular
BUSINESS_EMAIL=tu@nuevo-email.com
```
4. Guarda el archivo
5. Reinicia InstaFix

### Temas de la Aplicación
Para cambiar el tema visual:
1. Abre `.env`
2. Agrega o modifica:
```
THEME=nombre_del_tema
```
3. Temas disponibles: `cosmo`, `flatly`, `superhero`, `darkly`, `cyborg`

## Backup y Seguridad

### Respaldar Datos
Tus datos están en el archivo `instafix.db`:
1. **Ubicación**: Misma carpeta que InstaFix
2. **Backup**: Copia `instafix.db` a lugar seguro
3. **Frecuencia recomendada**: Diario o semanal
4. **Restaurar**: Reemplaza `instafix.db` con tu backup

### Migrar a Otra Computadora
1. **Copiar archivos**:
   - `instafix.db` (base de datos)
   - `.env` (configuración)
2. **Instalar InstaFix** en la nueva computadora
3. **Reemplazar archivos** copiados
4. **Ejecutar InstaFix**

## Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| `Ctrl+N` | Nueva reparación |
| `Ctrl+S` | Guardar reparación |
| `Ctrl+F` | Enfocar búsqueda |
| `F5` | Actualizar lista |
| `Delete` | Eliminar reparación seleccionada |
| `Enter` | Editar reparación seleccionada |
| `Escape` | Cerrar diálogo |

## Tips y Trucos

### Productividad
- **Usa la búsqueda**: Escribe parte del nombre o equipo para encontrar rápido
- **Ordena por columnas**: Clic en headers para ordenar
- **Doble clic**: En una reparación para editarla rápido

### Datos Consistentes
- **Formato de teléfonos**: Usa siempre el mismo formato
- **Nombres de marcas**: Mantén consistencia (Samsung vs samsung)
- **Tipos de equipo**: Usa las categorías predefinidas

### Organización
- **Numeración**: Los IDs se asignan automáticamente
- **Fechas**: Se registran automáticamente
- **Archivos PDF**: Se nombran automáticamente con fecha y cliente

## Solución de Problemas Comunes

### No se puede guardar reparación
**Problema**: Mensaje de error al guardar
**Solución**:
1. Verifica que todos los campos obligatorios estén completos
2. Revisa formato del teléfono
3. Asegúrate que el costo sea un número válido

### PDF no se genera
**Problema**: Error al crear PDF
**Solución**:
1. Verifica que el archivo `.env` esté configurado
2. Comprueba permisos de escritura en la carpeta
3. Cierra otros PDFs que puedan estar abiertos

### WhatsApp no abre
**Problema**: No se abre WhatsApp Web
**Solución**:
1. Verifica conexión a internet
2. Usa un navegador actualizado
3. Permite pop-ups en el navegador

### Aplicación lenta
**Problema**: InstaFix responde lentamente
**Solución**:
1. Cierra otros programas
2. Reinicia InstaFix
3. Considera hacer backup y limpiar base de datos antigua

### Datos perdidos
**Problema**: No aparecen reparaciones guardadas
**Solución**:
1. Verifica que el archivo `instafix.db` existe
2. Restaura desde backup si tienes
3. Revisa logs en `instafix.log` para más detalles

## Mantenimiento

### Limpieza Regular
- **Backup semanal**: De `instafix.db`
- **Limpiar PDFs antiguos**: Organiza archivos PDF generados
- **Revisar logs**: Elimina `instafix.log` si crece mucho

### Actualizaciones
- **Verificar versiones**: Revisa GitHub para nuevas versiones
- **Backup antes**: Siempre respalda datos antes de actualizar
- **Seguir instrucciones**: De instalación para nuevas versiones

---

¿Necesitas ayuda adicional? Contacta el soporte técnico o consulta la documentación técnica.