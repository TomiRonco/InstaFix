#!/usr/bin/env python3
"""
InstaFix - Sistema de Gestión de Reparaciones
Aplicación principal que inicia la interfaz gráfica
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import logging

# Agregar el directorio src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from gui.main_window import MainWindow
    from database.db_manager import DatabaseManager
    from dotenv import load_dotenv
except ImportError as e:
    messagebox.showerror("Error", f"Error al importar módulos: {e}")
    sys.exit(1)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instafix.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Función principal que inicia la aplicación"""
    try:
        # Cargar variables de entorno si existe el archivo
        if os.path.exists('.env'):
            load_dotenv()
        
        # Inicializar base de datos
        logger.info("Inicializando base de datos...")
        db_manager = DatabaseManager()
        db_manager.initialize_database()
        
        # Crear y ejecutar la aplicación
        logger.info("Iniciando aplicación InstaFix...")
        root = tk.Tk()
        app = MainWindow(root)
        
        # Configurar el cierre de la aplicación
        def on_closing():
            logger.info("Cerrando aplicación...")
            root.quit()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Iniciar el loop principal
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Error fatal: {e}")
        messagebox.showerror("Error Fatal", f"Error al iniciar la aplicación:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()