"""
Gestor de base de datos SQLite para InstaFix
Maneja todas las operaciones de base de datos
"""

import sqlite3
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Clase para gestionar la base de datos SQLite"""
    
    def __init__(self, db_path: str = "instafix.db"):
        """
        Inicializar el gestor de base de datos
        
        Args:
            db_path (str): Ruta al archivo de base de datos
        """
        self.db_path = db_path
        logger.info(f"Inicializando base de datos: {db_path}")
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtener una conexión a la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
            return conn
        except sqlite3.Error as e:
            logger.error(f"Error al conectar con la base de datos: {e}")
            raise
    
    def initialize_database(self):
        """Crear las tablas necesarias si no existen"""
        logger.info("Inicializando estructura de base de datos...")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla principal de reparaciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reparaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_presupuesto TEXT UNIQUE NOT NULL,
                    cliente_nombre TEXT NOT NULL,
                    cliente_apellido TEXT NOT NULL,
                    cliente_celular TEXT NOT NULL,
                    producto TEXT NOT NULL,
                    descripcion TEXT DEFAULT '',
                    costo_reparacion REAL DEFAULT NULL,
                    estado TEXT DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'en_proceso', 'finalizado', 'retirado')),
                    fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_retiro TIMESTAMP DEFAULT NULL,
                    notas TEXT DEFAULT ''
                )
            ''')
            
            # Tabla de historial de estados (para auditoría)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historial_estados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reparacion_id INTEGER NOT NULL,
                    estado_anterior TEXT,
                    estado_nuevo TEXT NOT NULL,
                    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notas TEXT DEFAULT '',
                    FOREIGN KEY (reparacion_id) REFERENCES reparaciones (id)
                )
            ''')
            
            # Tabla de configuración
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configuracion (
                    clave TEXT PRIMARY KEY,
                    valor TEXT NOT NULL,
                    descripcion TEXT DEFAULT '',
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insertar configuración por defecto
            cursor.execute('''
                INSERT OR IGNORE INTO configuracion (clave, valor, descripcion) 
                VALUES ('ultimo_numero_presupuesto', '0', 'Último número de presupuesto generado')
            ''')
            
            conn.commit()
            logger.info("Base de datos inicializada correctamente")
    
    def generar_numero_presupuesto(self) -> str:
        """Generar un nuevo número de presupuesto único"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Obtener el último número
            cursor.execute(
                "SELECT valor FROM configuracion WHERE clave = 'ultimo_numero_presupuesto'"
            )
            resultado = cursor.fetchone()
            
            if resultado:
                ultimo_numero = int(resultado[0])
            else:
                ultimo_numero = 0
            
            # Generar nuevo número
            nuevo_numero = ultimo_numero + 1
            numero_presupuesto = f"INF-{nuevo_numero:06d}"
            
            # Actualizar en la base de datos
            cursor.execute(
                "UPDATE configuracion SET valor = ?, fecha_actualizacion = CURRENT_TIMESTAMP WHERE clave = 'ultimo_numero_presupuesto'",
                (str(nuevo_numero),)
            )
            
            conn.commit()
            return numero_presupuesto
    
    def crear_reparacion(self, datos: Dict) -> str:
        """
        Crear una nueva reparación
        
        Args:
            datos (Dict): Datos de la reparación
            
        Returns:
            str: Número de presupuesto generado
        """
        numero_presupuesto = self.generar_numero_presupuesto()
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO reparaciones (
                    numero_presupuesto, cliente_nombre, cliente_apellido, 
                    cliente_celular, producto, descripcion, costo_reparacion, estado
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                numero_presupuesto,
                datos['cliente_nombre'],
                datos['cliente_apellido'],
                datos['cliente_celular'],
                datos['producto'],
                datos.get('descripcion', ''),
                datos.get('costo_reparacion'),
                datos.get('estado', 'pendiente')
            ))
            
            reparacion_id = cursor.lastrowid
            
            # Registrar en historial
            cursor.execute('''
                INSERT INTO historial_estados (reparacion_id, estado_nuevo, notas)
                VALUES (?, ?, ?)
            ''', (reparacion_id, datos.get('estado', 'pendiente'), 'Reparación creada'))
            
            conn.commit()
            logger.info(f"Reparación creada: {numero_presupuesto}")
            
        return numero_presupuesto
    
    def obtener_todas_reparaciones(self) -> List[Dict]:
        """Obtener todas las reparaciones"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM reparaciones 
                ORDER BY fecha_ingreso DESC
            ''')
            
            reparaciones = []
            for row in cursor.fetchall():
                reparacion = dict(row)
                reparaciones.append(reparacion)
            
            return reparaciones
    
    def buscar_reparaciones(self, termino: str) -> List[Dict]:
        """
        Buscar reparaciones por término
        
        Args:
            termino (str): Término de búsqueda
            
        Returns:
            List[Dict]: Lista de reparaciones que coinciden
        """
        termino = f"%{termino}%"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM reparaciones 
                WHERE numero_presupuesto LIKE ? 
                   OR cliente_nombre LIKE ? 
                   OR cliente_apellido LIKE ? 
                   OR cliente_celular LIKE ?
                   OR producto LIKE ?
                ORDER BY fecha_ingreso DESC
            ''', (termino, termino, termino, termino, termino))
            
            reparaciones = []
            for row in cursor.fetchall():
                reparacion = dict(row)
                reparaciones.append(reparacion)
            
            return reparaciones
    
    def obtener_reparacion(self, numero_presupuesto: str) -> Optional[Dict]:
        """Obtener una reparación específica"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM reparaciones WHERE numero_presupuesto = ?",
                (numero_presupuesto,)
            )
            
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    def actualizar_reparacion(self, numero_presupuesto: str, datos: Dict) -> bool:
        """
        Actualizar una reparación existente
        
        Args:
            numero_presupuesto (str): Número de presupuesto
            datos (Dict): Nuevos datos
            
        Returns:
            bool: True si se actualizó correctamente
        """
        # Obtener estado actual para el historial
        reparacion_actual = self.obtener_reparacion(numero_presupuesto)
        if not reparacion_actual:
            return False
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Construir la consulta de actualización dinámicamente
            campos = []
            valores = []
            
            for campo, valor in datos.items():
                if campo in ['cliente_nombre', 'cliente_apellido', 'cliente_celular', 
                           'producto', 'descripcion', 'costo_reparacion', 'estado', 'notas']:
                    campos.append(f"{campo} = ?")
                    valores.append(valor)
            
            if not campos:
                return False
            
            campos.append("fecha_actualizacion = CURRENT_TIMESTAMP")
            valores.append(numero_presupuesto)
            
            consulta = f"UPDATE reparaciones SET {', '.join(campos)} WHERE numero_presupuesto = ?"
            cursor.execute(consulta, valores)
            
            # Si cambió el estado, registrar en historial
            if 'estado' in datos and datos['estado'] != reparacion_actual['estado']:
                cursor.execute('''
                    INSERT INTO historial_estados (reparacion_id, estado_anterior, estado_nuevo, notas)
                    VALUES (?, ?, ?, ?)
                ''', (
                    reparacion_actual['id'],
                    reparacion_actual['estado'],
                    datos['estado'],
                    f"Estado cambiado a {datos['estado']}"
                ))
            
            # Si se marca como retirado, actualizar fecha de retiro
            if 'estado' in datos and datos['estado'] == 'retirado':
                cursor.execute(
                    "UPDATE reparaciones SET fecha_retiro = CURRENT_TIMESTAMP WHERE numero_presupuesto = ?",
                    (numero_presupuesto,)
                )
            
            conn.commit()
            logger.info(f"Reparación actualizada: {numero_presupuesto}")
            return cursor.rowcount > 0
    
    def eliminar_reparacion(self, numero_presupuesto: str) -> bool:
        """Eliminar una reparación (soft delete - cambiar estado)"""
        return self.actualizar_reparacion(numero_presupuesto, {'estado': 'eliminado'})
    
    def obtener_estadisticas(self) -> Dict:
        """Obtener estadísticas básicas"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Contar por estado
            cursor.execute('''
                SELECT estado, COUNT(*) as cantidad 
                FROM reparaciones 
                WHERE estado != 'eliminado'
                GROUP BY estado
            ''')
            
            estadisticas = {
                'pendiente': 0,
                'en_proceso': 0,
                'finalizado': 0,
                'retirado': 0,
                'total': 0
            }
            
            for row in cursor.fetchall():
                estado, cantidad = row
                estadisticas[estado] = cantidad
                estadisticas['total'] += cantidad
            
            return estadisticas