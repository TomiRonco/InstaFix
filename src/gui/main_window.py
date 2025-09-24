"""
Ventana principal de InstaFix
Interfaz gráfica moderna y minimalista
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import logging
from typing import Optional, List, Dict
from datetime import datetime
import sys
import os
import subprocess
import tempfile
import platform
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from whatsapp.client import WhatsAppClient
from .dialogs import ReparacionDialog, ConfigDialog

logger = logging.getLogger(__name__)

def maximize_window(window):
    """
    Función auxiliar para maximizar una ventana de forma multiplataforma
    
    Args:
        window: Ventana de Tkinter a maximizar
    """
    try:
        # Para macOS
        window.attributes('-zoomed', True)
    except tk.TclError:
        try:
            # Para Windows/Linux
            window.state('zoomed')
        except tk.TclError:
            # Fallback: pantalla completa manual
            window.update_idletasks()
            width = window.winfo_screenwidth()
            height = window.winfo_screenheight()
            window.geometry(f"{width}x{height}+0+0")

class MainWindow:
    """Ventana principal de la aplicación"""
    
    def __init__(self, root: tk.Tk):
        """
        Inicializar la ventana principal
        
        Args:
            root (tk.Tk): Ventana raíz de Tkinter
        """
        self.root = root
        self.db_manager = DatabaseManager()
        self.whatsapp_client = WhatsAppClient()
        
        # Configurar ventana principal
        self._setup_window()
        
        # Crear interfaz
        self._create_menu()
        self._create_toolbar()
        self._create_main_content()
        self._create_status_bar()
        
        # Cargar datos iniciales
        self._load_data()
        
        logger.info("Ventana principal inicializada")
    
    def _setup_window(self):
        """Configurar la ventana principal"""
        # Obtener nombre del negocio desde configuración
        business_name = os.getenv('BUSINESS_NAME', 'InstaFix')
        self.root.title(f"{business_name} - Sistema de Gestión de Reparaciones")
        self.root.geometry("1200x700")
        self.root.minsize(900, 600)
        
        # Maximizar ventana
        maximize_window(self.root)
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores personalizados
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Arial', 10))
        style.configure('Status.TLabel', font=('Arial', 9))
    
    def _create_menu(self):
        """Crear la barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nueva Reparación", command=self._nueva_reparacion, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Exportar...", command=self._exportar_datos)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Menú Ver
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver", menu=view_menu)
        view_menu.add_command(label="Actualizar", command=self._load_data, accelerator="F5")
        view_menu.add_separator()
        view_menu.add_command(label="Estadísticas", command=self._mostrar_estadisticas)
        
        # Menú Herramientas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        tools_menu.add_command(label="⚙️ Configuración", command=self._mostrar_configuracion)
        tools_menu.add_separator()
        tools_menu.add_command(label="📱 Probar WhatsApp Web", command=self._test_whatsapp)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self._mostrar_acerca_de)
        
        # Atajos de teclado
        self.root.bind('<Control-n>', lambda e: self._nueva_reparacion())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<F5>', lambda e: self._load_data())
    
    def _create_toolbar(self):
        """Crear la barra de herramientas"""
        toolbar_frame = ttk.Frame(self.root)
        toolbar_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Título
        business_name = os.getenv('BUSINESS_NAME', 'InstaFix')
        title_label = ttk.Label(toolbar_frame, text=business_name, style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Subtítulo
        subtitle_label = ttk.Label(toolbar_frame, text="Sistema de Gestión de Reparaciones", 
                                 style='Subtitle.TLabel')
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Botones principales
        buttons_frame = ttk.Frame(toolbar_frame)
        buttons_frame.pack(side=tk.RIGHT)
        
        # Botón Nueva Reparación
        self.btn_nueva = ttk.Button(buttons_frame, text="➕ Nueva Reparación", 
                                   command=self._nueva_reparacion)
        self.btn_nueva.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botón Actualizar
        self.btn_actualizar = ttk.Button(buttons_frame, text="🔄 Actualizar", 
                                       command=self._load_data)
        self.btn_actualizar.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botón Imprimir
        self.btn_imprimir = ttk.Button(buttons_frame, text="🖨️ Imprimir", 
                                     command=self._imprimir_presupuesto)
        self.btn_imprimir.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botón Configuración
        self.btn_config = ttk.Button(buttons_frame, text="⚙️ Configuración", 
                                   command=self._mostrar_configuracion)
        self.btn_config.pack(side=tk.LEFT)
    
    def _create_main_content(self):
        """Crear el contenido principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Frame de búsqueda
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍 Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_change)
        
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón limpiar búsqueda
        ttk.Button(search_frame, text="✖️ Limpiar", 
                  command=self._clear_search).pack(side=tk.LEFT)
        
        # Filtros de estado
        ttk.Label(search_frame, text="Estado:").pack(side=tk.LEFT, padx=(20, 5))
        
        self.filter_var = tk.StringVar(value="todos")
        filter_combo = ttk.Combobox(search_frame, textvariable=self.filter_var, 
                                   values=["todos", "pendiente", "en_proceso", "finalizado", "retirado"],
                                   state="readonly", width=12)
        filter_combo.pack(side=tk.LEFT)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self._load_data())
        
        # Tabla de reparaciones
        self._create_treeview(main_frame)
    
    def _create_treeview(self, parent):
        """Crear la tabla de reparaciones"""
        # Frame para la tabla y scrollbars
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Definir columnas
        columns = (
            'numero_presupuesto', 'cliente_nombre', 'cliente_apellido', 
            'cliente_celular', 'producto', 'costo_reparacion', 'estado', 'fecha_ingreso'
        )
        
        # Crear Treeview
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.tree.heading('numero_presupuesto', text='N° Presupuesto', anchor=tk.W)
        self.tree.heading('cliente_nombre', text='Nombre', anchor=tk.W)
        self.tree.heading('cliente_apellido', text='Apellido', anchor=tk.W)
        self.tree.heading('cliente_celular', text='Celular', anchor=tk.W)
        self.tree.heading('producto', text='Producto', anchor=tk.W)
        self.tree.heading('costo_reparacion', text='Costo', anchor=tk.E)
        self.tree.heading('estado', text='Estado', anchor=tk.CENTER)
        self.tree.heading('fecha_ingreso', text='Fecha Ingreso', anchor=tk.CENTER)
        
        # Configurar anchos de columnas
        self.tree.column('numero_presupuesto', width=120, minwidth=120)
        self.tree.column('cliente_nombre', width=120, minwidth=100)
        self.tree.column('cliente_apellido', width=120, minwidth=100)
        self.tree.column('cliente_celular', width=110, minwidth=100)
        self.tree.column('producto', width=150, minwidth=120)
        self.tree.column('costo_reparacion', width=80, minwidth=80)
        self.tree.column('estado', width=100, minwidth=90)
        self.tree.column('fecha_ingreso', width=120, minwidth=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Posicionar elementos
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configurar grid
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Eventos
        self.tree.bind('<Double-1>', self._on_item_double_click)
        self.tree.bind('<Button-3>', self._on_right_click)  # Click derecho
        
        # Menú contextual
        self._create_context_menu()
    
    def _create_context_menu(self):
        """Crear menú contextual para la tabla"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="✏️ Editar", command=self._editar_reparacion)
        self.context_menu.add_command(label="🔄 Cambiar Estado", command=self._cambiar_estado)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📱 Enviar por WhatsApp", command=self._enviar_whatsapp_menu)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📋 Ver Historial", command=self._ver_historial)
    
    def _create_status_bar(self):
        """Crear la barra de estado"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Separador
        ttk.Separator(status_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(5, 0))
        
        # Contenedor de estado
        status_content = ttk.Frame(status_frame)
        status_content.pack(fill=tk.X, padx=10, pady=5)
        
        # Texto de estado principal
        self.status_text = tk.StringVar(value="Listo")
        status_label = ttk.Label(status_content, textvariable=self.status_text, style='Status.TLabel')
        status_label.pack(side=tk.LEFT)
        
        # Contador de registros
        self.count_text = tk.StringVar(value="0 reparaciones")
        count_label = ttk.Label(status_content, textvariable=self.count_text, style='Status.TLabel')
        count_label.pack(side=tk.RIGHT)
        
        # Indicador WhatsApp (siempre habilitado para WhatsApp Web)
        self.whatsapp_status = tk.StringVar(value="WhatsApp: ✅ WhatsApp Web disponible")
        whatsapp_label = ttk.Label(status_content, textvariable=self.whatsapp_status, 
                                 style='Status.TLabel')
        whatsapp_label.pack(side=tk.RIGHT, padx=(0, 20))
    
    def _load_data(self):
        """Cargar datos en la tabla"""
        try:
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtener filtro de estado
            estado_filtro = self.filter_var.get()
            
            # Obtener datos
            if self.search_var.get().strip():
                reparaciones = self.db_manager.buscar_reparaciones(self.search_var.get().strip())
            else:
                reparaciones = self.db_manager.obtener_todas_reparaciones()
            
            # Aplicar filtro de estado
            if estado_filtro != "todos":
                reparaciones = [r for r in reparaciones if r['estado'] == estado_filtro]
            
            # Insertar datos en la tabla
            for reparacion in reparaciones:
                # Formatear datos
                numero = reparacion['numero_presupuesto']
                nombre = reparacion['cliente_nombre']
                apellido = reparacion['cliente_apellido']
                celular = reparacion['cliente_celular']
                producto = reparacion['producto']
                
                # Formatear costo
                costo = reparacion['costo_reparacion']
                if costo is not None:
                    costo_str = f"${costo:,.2f}"
                else:
                    costo_str = "-"
                
                # Formatear estado
                estado = reparacion['estado'].title()
                if estado == 'En_Proceso':
                    estado = 'En Proceso'
                
                # Formatear fecha
                fecha_str = reparacion['fecha_ingreso'][:10]  # Solo la fecha, sin hora
                
                # Configurar tags para colores
                tag = self._get_estado_tag(reparacion['estado'])
                
                item = self.tree.insert('', tk.END, values=(
                    numero, nombre, apellido, celular, producto, costo_str, estado, fecha_str
                ), tags=(tag,))
            
            # Configurar colores por estado
            self._configure_row_colors()
            
            # Actualizar contador
            self.count_text.set(f"{len(reparaciones)} reparaciones")
            self.status_text.set("Datos cargados correctamente")
            
            logger.info(f"Cargadas {len(reparaciones)} reparaciones")
            
        except Exception as e:
            logger.error(f"Error al cargar datos: {e}")
            messagebox.showerror("Error", f"Error al cargar datos:\n{e}")
    
    def _get_estado_tag(self, estado: str) -> str:
        """Obtener tag de color según el estado"""
        return f"estado_{estado}"
    
    def _configure_row_colors(self):
        """Configurar colores de filas según estado"""
        self.tree.tag_configure('estado_pendiente', background='#fff2cc')
        self.tree.tag_configure('estado_en_proceso', background='#d4edda')
        self.tree.tag_configure('estado_finalizado', background='#cce5ff')
        self.tree.tag_configure('estado_retirado', background='#e2e3e5')
    
    def _on_search_change(self, *args):
        """Evento cuando cambia el texto de búsqueda"""
        # Realizar búsqueda con delay
        if hasattr(self, '_search_timer'):
            self.root.after_cancel(self._search_timer)
        
        self._search_timer = self.root.after(500, self._load_data)
    
    def _clear_search(self):
        """Limpiar búsqueda"""
        self.search_var.set("")
        self.filter_var.set("todos")
        self._load_data()
    
    def _on_item_double_click(self, event):
        """Evento de doble click en un elemento"""
        self._editar_reparacion()
    
    def _on_right_click(self, event):
        """Evento de click derecho"""
        # Seleccionar el elemento bajo el cursor
        item = self.tree.identify('item', event.x, event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def _nueva_reparacion(self):
        """Crear nueva reparación"""
        dialog = ReparacionDialog(self.root, "Nueva Reparación")
        if dialog.result:
            try:
                numero = self.db_manager.crear_reparacion(dialog.result)
                self._load_data()
                self.status_text.set(f"Reparación {numero} creada correctamente")
                messagebox.showinfo("Éxito", f"Reparación {numero} creada correctamente")
            except Exception as e:
                logger.error(f"Error al crear reparación: {e}")
                messagebox.showerror("Error", f"Error al crear reparación:\n{e}")
    
    def _editar_reparacion(self):
        """Editar reparación seleccionada"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una reparación para editar")
            return
        
        # Obtener datos de la reparación seleccionada
        item = selection[0]
        valores = self.tree.item(item, 'values')
        numero_presupuesto = valores[0]
        
        # Obtener datos completos de la base de datos
        reparacion = self.db_manager.obtener_reparacion(numero_presupuesto)
        if not reparacion:
            messagebox.showerror("Error", "No se pudo obtener los datos de la reparación")
            return
        
        # Abrir diálogo de edición
        dialog = ReparacionDialog(self.root, "Editar Reparación", reparacion)
        if dialog.result:
            try:
                # Verificar cambios importantes para notificaciones
                estado_anterior = reparacion['estado']
                costo_anterior = reparacion['costo_reparacion']
                
                # Actualizar en base de datos
                if self.db_manager.actualizar_reparacion(numero_presupuesto, dialog.result):
                    self._load_data()
                    self.status_text.set(f"Reparación {numero_presupuesto} actualizada")
                    
                    # Enviar notificaciones automáticas si corresponde
                    self._check_and_send_notifications(
                        dialog.result, estado_anterior, costo_anterior
                    )
                    
                else:
                    messagebox.showerror("Error", "No se pudo actualizar la reparación")
                    
            except Exception as e:
                logger.error(f"Error al actualizar reparación: {e}")
                messagebox.showerror("Error", f"Error al actualizar reparación:\n{e}")
    
    def _check_and_send_notifications(self, datos: Dict, estado_anterior: str, costo_anterior: Optional[float]):
        """Verificar y mostrar opciones de notificaciones automáticas"""
        try:
            notificaciones_pendientes = []
            
            # Notificación por costo definido
            if (costo_anterior is None and 
                datos.get('costo_reparacion') is not None and 
                datos.get('costo_reparacion') > 0):
                notificaciones_pendientes.append("costo")
            
            # Notificación por estado finalizado
            if (estado_anterior != 'finalizado' and 
                datos.get('estado') == 'finalizado'):
                notificaciones_pendientes.append("finalizado")
            
            # Si hay notificaciones pendientes, preguntar si quiere enviarlas
            if notificaciones_pendientes:
                mensaje_pregunta = "¿Deseas abrir WhatsApp para enviar notificaciones?\n\n"
                
                if "costo" in notificaciones_pendientes:
                    mensaje_pregunta += "💰 Notificación de costo definido\n"
                
                if "finalizado" in notificaciones_pendientes:
                    mensaje_pregunta += "✅ Notificación de reparación finalizada\n"
                
                mensaje_pregunta += "\nSe abrirá WhatsApp Web con el mensaje listo para enviar."
                
                respuesta = messagebox.askyesno(
                    "📱 Enviar Notificación WhatsApp",
                    mensaje_pregunta
                )
                
                if respuesta:
                    # Abrir WhatsApp con el primer mensaje disponible
                    if "costo" in notificaciones_pendientes:
                        self.whatsapp_client.enviar_notificacion_costo(
                            datos['cliente_nombre'],
                            datos['cliente_apellido'],
                            datos['cliente_celular'],
                            datos['producto'],
                            datos['costo_reparacion'],
                            datos.get('notas', '')  # Usar notas en lugar de descripcion
                        )
                    elif "finalizado" in notificaciones_pendientes:
                        self.whatsapp_client.enviar_notificacion_finalizado(
                            datos['cliente_nombre'],
                            datos['cliente_apellido'],
                            datos['cliente_celular'],
                            datos['producto']
                        )
                    
                    messagebox.showinfo("📱 WhatsApp Abierto", 
                                      "WhatsApp Web se abrió con el mensaje listo.\n\n"
                                      "Solo presiona ENTER para enviarlo.")
            
            # Para retiro, pregunta opcional
            if (estado_anterior != 'retirado' and 
                datos.get('estado') == 'retirado'):
                
                respuesta = messagebox.askyesno(
                    "📦 Confirmar Retiro",
                    "¿Deseas enviar una confirmación de retiro por WhatsApp?\n\n"
                    "Se abrirá WhatsApp Web con el mensaje de confirmación."
                )
                
                if respuesta:
                    self.whatsapp_client.enviar_notificacion_retirado(
                        datos['cliente_nombre'],
                        datos['cliente_apellido'],
                        datos['cliente_celular'],
                        datos['producto']
                    )
                    messagebox.showinfo("📱 WhatsApp Abierto", 
                                      "WhatsApp Web se abrió con la confirmación de retiro.\n\n"
                                      "Solo presiona ENTER para enviarlo.")
            
        except Exception as e:
            logger.error(f"Error al procesar notificaciones: {e}")
            messagebox.showwarning("Advertencia", f"Error al abrir WhatsApp:\n{e}")
    
    def _cambiar_estado(self):
        """Cambiar estado de reparación seleccionada"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una reparación")
            return
        
        # Obtener número de presupuesto
        item = selection[0]
        valores = self.tree.item(item, 'values')
        numero_presupuesto = valores[0]
        
        # Diálogo para seleccionar nuevo estado
        estados = ['pendiente', 'en_proceso', 'finalizado', 'retirado']
        nuevo_estado = simpledialog.askstring(
            "Cambiar Estado",
            f"Estado actual: {valores[6]}\n\nNuevo estado:",
            initialvalue=valores[6].lower().replace(' ', '_')
        )
        
        if nuevo_estado and nuevo_estado in estados:
            try:
                # Obtener datos actuales
                reparacion = self.db_manager.obtener_reparacion(numero_presupuesto)
                estado_anterior = reparacion['estado']
                
                # Actualizar estado
                if self.db_manager.actualizar_reparacion(numero_presupuesto, {'estado': nuevo_estado}):
                    self._load_data()
                    self.status_text.set(f"Estado actualizado a: {nuevo_estado}")
                    
                    # Verificar notificaciones
                    self._check_and_send_notifications(
                        {**reparacion, 'estado': nuevo_estado}, 
                        estado_anterior, 
                        reparacion['costo_reparacion']
                    )
                
            except Exception as e:
                logger.error(f"Error al cambiar estado: {e}")
                messagebox.showerror("Error", f"Error al cambiar estado:\n{e}")
    
    def _enviar_whatsapp_menu(self):
        """Menú para enviar mensajes por WhatsApp Web"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una reparación")
            return
        
        # Obtener datos
        item = selection[0]
        valores = self.tree.item(item, 'values')
        numero_presupuesto = valores[0]
        
        reparacion = self.db_manager.obtener_reparacion(numero_presupuesto)
        if not reparacion:
            messagebox.showerror("Error", "No se pudieron obtener los datos")
            return
        
        # Crear ventana de opciones
        dialog = tk.Toplevel(self.root)
        dialog.title("📱 Enviar por WhatsApp")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (300)
        y = (dialog.winfo_screenheight() // 2) - (250)
        dialog.geometry(f"600x500+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text=f"📱 Enviar WhatsApp a {reparacion['cliente_nombre']} {reparacion['cliente_apellido']}", 
                 font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        ttk.Label(main_frame, text=f"📞 Celular: {reparacion['cliente_celular']}", 
                 font=('Arial', 10)).pack(pady=(0, 20))
        
        # Opciones de mensaje
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Mensaje de Costo
        if reparacion['costo_reparacion']:
            costo_frame = ttk.Frame(notebook, padding="10")
            notebook.add(costo_frame, text="💰 Notificar Costo")
            
            mensaje_costo = self.whatsapp_client._generar_mensaje_costo(
                reparacion['cliente_nombre'],
                reparacion['cliente_apellido'],
                reparacion['producto'],
                reparacion['costo_reparacion'],
                reparacion.get('notas', '')  # Usar notas (mensaje para cliente) en lugar de descripcion
            )
            
            costo_text = tk.Text(costo_frame, height=15, wrap=tk.WORD, font=('Arial', 10))
            costo_text.pack(fill=tk.BOTH, expand=True)
            costo_text.insert(tk.END, mensaje_costo)
            costo_text.config(state='disabled')
            
            ttk.Button(costo_frame, text="📱 Abrir WhatsApp Web", 
                      command=lambda: self._abrir_whatsapp_con_mensaje(reparacion['cliente_celular'], mensaje_costo, dialog)).pack(pady=(10, 0))
        
        # Mensaje Finalizado
        if reparacion['estado'] in ['finalizado', 'retirado']:
            finalizado_frame = ttk.Frame(notebook, padding="10")
            notebook.add(finalizado_frame, text="✅ Notificar Finalizado")
            
            mensaje_finalizado = self.whatsapp_client._generar_mensaje_finalizado(
                reparacion['cliente_nombre'],
                reparacion['cliente_apellido'],
                reparacion['producto']
            )
            
            finalizado_text = tk.Text(finalizado_frame, height=15, wrap=tk.WORD, font=('Arial', 10))
            finalizado_text.pack(fill=tk.BOTH, expand=True)
            finalizado_text.insert(tk.END, mensaje_finalizado)
            finalizado_text.config(state='disabled')
            
            ttk.Button(finalizado_frame, text="📱 Abrir WhatsApp Web", 
                      command=lambda: self._abrir_whatsapp_con_mensaje(reparacion['cliente_celular'], mensaje_finalizado, dialog)).pack(pady=(10, 0))
        
        # Mensaje Personalizado
        personalizado_frame = ttk.Frame(notebook, padding="10")
        notebook.add(personalizado_frame, text="✏️ Mensaje Personalizado")
        
        ttk.Label(personalizado_frame, text="Escribe tu mensaje personalizado:").pack(anchor=tk.W)
        
        mensaje_personalizado = tk.Text(personalizado_frame, height=10, wrap=tk.WORD, font=('Arial', 10))
        mensaje_personalizado.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # Mensaje ejemplo por defecto
        mensaje_ejemplo = f"Hola {reparacion['cliente_nombre']}!\n\nTe escribo desde {self.whatsapp_client.business_name} sobre tu {reparacion['producto']}.\n\n"
        mensaje_personalizado.insert(tk.END, mensaje_ejemplo)
        
        def enviar_personalizado():
            mensaje = mensaje_personalizado.get(1.0, tk.END).strip()
            if mensaje:
                self._abrir_whatsapp_con_mensaje(reparacion['cliente_celular'], mensaje, dialog)
            else:
                messagebox.showwarning("Advertencia", "Escribe un mensaje")
        
        ttk.Button(personalizado_frame, text="📱 Abrir WhatsApp Web", 
                  command=enviar_personalizado).pack(pady=(10, 0))
        
        # Botón cerrar
        ttk.Button(main_frame, text="Cerrar", command=dialog.destroy).pack(pady=(10, 0))
    
    def _abrir_whatsapp_con_mensaje(self, celular: str, mensaje: str, dialog: tk.Toplevel):
        """Abrir WhatsApp Web con mensaje pre-escrito"""
        try:
            success = self.whatsapp_client._send_message_whatsapp_web(celular, mensaje)
            if success:
                dialog.destroy()
                messagebox.showinfo("✅ WhatsApp Abierto", 
                                  f"WhatsApp Web se abrió con el mensaje listo.\n\n"
                                  f"Solo presiona ENTER para enviar el mensaje al cliente.")
            else:
                messagebox.showerror("Error", "No se pudo abrir WhatsApp Web")
        except Exception as e:
            logger.error(f"Error al abrir WhatsApp: {e}")
            messagebox.showerror("Error", f"Error al abrir WhatsApp Web:\n{e}")
    
    def _ver_historial(self):
        """Ver historial de una reparación"""
        messagebox.showinfo("Próximamente", "Funcionalidad de historial en desarrollo")
    
    def _exportar_datos(self):
        """Exportar datos a CSV"""
        from tkinter import filedialog
        import csv
        
        try:
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Exportar datos"
            )
            
            if archivo:
                reparaciones = self.db_manager.obtener_todas_reparaciones()
                
                with open(archivo, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = [
                        'numero_presupuesto', 'cliente_nombre', 'cliente_apellido',
                        'cliente_celular', 'producto', 'descripcion', 'costo_reparacion',
                        'estado', 'fecha_ingreso', 'fecha_actualizacion', 'fecha_retiro'
                    ]
                    
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for reparacion in reparaciones:
                        writer.writerow(reparacion)
                
                messagebox.showinfo("Éxito", f"Datos exportados a:\n{archivo}")
                
        except Exception as e:
            logger.error(f"Error al exportar: {e}")
            messagebox.showerror("Error", f"Error al exportar:\n{e}")
    
    def _test_whatsapp(self):
        """Probar WhatsApp Web"""
        if self.whatsapp_client.test_connection():
            messagebox.showinfo("✅ WhatsApp Disponible", 
                              "WhatsApp Web se abrió correctamente.\n\n"
                              "El sistema está listo para enviar mensajes.")
        else:
            messagebox.showerror("❌ Error", 
                               "No se pudo abrir WhatsApp Web.\n\n"
                               "Verifica que tengas un navegador instalado.")
    
    def _mostrar_estadisticas(self):
        """Mostrar estadísticas básicas"""
        try:
            stats = self.db_manager.obtener_estadisticas()
            
            mensaje = "📊 ESTADÍSTICAS\n\n"
            mensaje += f"📋 Total de reparaciones: {stats['total']}\n"
            mensaje += f"⏳ Pendientes: {stats['pendiente']}\n"
            mensaje += f"🔧 En proceso: {stats['en_proceso']}\n"
            mensaje += f"✅ Finalizadas: {stats['finalizado']}\n"
            mensaje += f"📦 Retiradas: {stats['retirado']}\n"
            
            messagebox.showinfo("Estadísticas", mensaje)
            
        except Exception as e:
            logger.error(f"Error al obtener estadísticas: {e}")
            messagebox.showerror("Error", f"Error al obtener estadísticas:\n{e}")
    
    def _mostrar_configuracion(self):
        """Mostrar diálogo de configuración"""
        try:
            from .dialogs import ConfigDialog
            dialog = ConfigDialog(self.root)
            
            if dialog.result:
                # Guardar configuración en archivo .env
                self._guardar_configuracion(dialog.result)
                
                # Recargar configuración en WhatsApp client
                if self.whatsapp_client:
                    self.whatsapp_client.business_name = dialog.result.get('business_name', 'InstaFix')
                    self.whatsapp_client.business_slogan = dialog.result.get('business_slogan', '')
                    self.whatsapp_client.business_hours = dialog.result.get('business_hours', 'Lunes a Viernes 9:00-18:00')
                    self.whatsapp_client.business_address = dialog.result.get('business_address', '')
                    self.whatsapp_client.business_phone = dialog.result.get('business_phone', '')
                    self.whatsapp_client.business_email = dialog.result.get('business_email', '')
                    self.whatsapp_client.business_mobile = dialog.result.get('business_mobile', '')
                    self.whatsapp_client.business_extra = dialog.result.get('business_extra', '')
                
                # Actualizar título de la ventana con el nuevo nombre del negocio
                self._actualizar_titulos()
                
                messagebox.showinfo("Configuración", "Configuración guardada correctamente.\nLos cambios se aplicarán en los próximos mensajes de WhatsApp.")
                
        except Exception as e:
            logger.error(f"Error al mostrar configuración: {e}")
            messagebox.showerror("Error", f"Error al mostrar configuración:\n{e}")
    
    def _guardar_configuracion(self, config: dict):
        """Guardar configuración en archivo .env"""
        try:
            env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
            
            lines = []
            lines.append("# Variables de entorno para InstaFix")
            lines.append("# Configuración del negocio")
            lines.append(f"BUSINESS_NAME={config.get('business_name', 'InstaFix')}")
            lines.append(f"BUSINESS_SLOGAN={config.get('business_slogan', '')}")
            lines.append(f"BUSINESS_HOURS={config.get('business_hours', 'Lunes a Viernes 9:00-18:00')}")
            lines.append(f"BUSINESS_ADDRESS={config.get('business_address', '')}")
            lines.append(f"BUSINESS_PHONE={config.get('business_phone', '')}")
            lines.append(f"BUSINESS_MOBILE={config.get('business_mobile', '')}")
            lines.append(f"BUSINESS_EMAIL={config.get('business_email', '')}")
            lines.append(f"BUSINESS_EXTRA={config.get('business_extra', '')}")
            lines.append("")
            lines.append("# WhatsApp Web no requiere tokens o configuración adicional")
            lines.append("# Solo se necesita tener WhatsApp Web disponible en el navegador")
            
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
                
            logger.info("Configuración guardada en .env")
            
        except Exception as e:
            logger.error(f"Error al guardar configuración: {e}")
            raise
    
    def _mostrar_acerca_de(self):
        """Mostrar información sobre la aplicación"""
        business_name = os.getenv('BUSINESS_NAME', 'InstaFix')
        mensaje = f"""🔧 {business_name}
Sistema de Gestión de Reparaciones

Versión: 1.0.0

Características:
• Gestión completa de reparaciones
• Notificaciones por WhatsApp Web
• Interfaz moderna y minimalista
• Base de datos local SQLite
• Exportación de datos

📱 WhatsApp Web Integration:
Los mensajes se abren automáticamente en
WhatsApp Web listos para enviar.

Desarrollado con ❤️ para hacer más fácil
la gestión de tu negocio de reparaciones."""
        
        messagebox.showinfo(f"Acerca de {business_name}", mensaje)
    
    
    
    def _actualizar_titulos(self):
        """Actualizar los títulos de la ventana con el nombre del negocio actual"""
        business_name = os.getenv('BUSINESS_NAME', 'InstaFix')
        
        # Actualizar título de la ventana principal
        self.root.title(f"{business_name} - Sistema de Gestión de Reparaciones")
        
        # Actualizar título en la barra de herramientas
        # Buscar el widget del título y actualizarlo
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label) and 'Title.TLabel' in str(child.cget('style')):
                        child.config(text=business_name)
                        break
    
    def _imprimir_presupuesto(self):
        """Imprimir presupuesto seleccionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un presupuesto para imprimir")
            return
        
        # Obtener datos del presupuesto seleccionado
        item = selection[0]
        valores = self.tree.item(item, 'values')
        numero_presupuesto = valores[0]
        
        # Obtener datos completos de la base de datos
        reparacion = self.db_manager.obtener_reparacion(numero_presupuesto)
        if not reparacion:
            messagebox.showerror("Error", "No se pudieron obtener los datos del presupuesto")
            return
        
        try:
            # Generar PDF
            pdf_path = self._generar_pdf_presupuesto(reparacion)
            
            # Abrir el PDF generado
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", pdf_path])
            elif platform.system() == "Windows":
                os.startfile(pdf_path)
            else:  # Linux
                subprocess.run(["xdg-open", pdf_path])
            
            messagebox.showinfo("PDF Generado", f"Presupuesto impreso correctamente:\n{pdf_path}")
            
        except Exception as e:
            logger.error(f"Error al generar PDF: {e}")
            messagebox.showerror("Error", f"Error al generar PDF:\n{e}")
    
    def _generar_pdf_presupuesto(self, reparacion: Dict) -> str:
        """Generar PDF con formato profesional - Original y Copia"""
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', 
                                       prefix=f"presupuesto_{reparacion['numero_presupuesto']}_") as tmp:
            pdf_path = tmp.name
        
        # Obtener datos del negocio
        business_name = os.getenv('BUSINESS_NAME', 'InstaFix')
        business_address = os.getenv('BUSINESS_ADDRESS', '')
        business_phone = os.getenv('BUSINESS_PHONE', '')
        business_mobile = os.getenv('BUSINESS_MOBILE', '')
        business_email = os.getenv('BUSINESS_EMAIL', '')
        
        # Formatear fecha
        fecha_ingreso = datetime.strptime(reparacion['fecha_ingreso'], '%Y-%m-%d %H:%M:%S')
        fecha_formateada = fecha_ingreso.strftime('%d/%m/%Y')
        
        # Crear canvas
        c = canvas.Canvas(pdf_path, pagesize=A4)
        page_width, page_height = A4
        
        # Dividir la página en dos mitades
        mitad_altura = page_height / 2
        
        # Dibujar ORIGINAL (mitad superior) - más espacio desde arriba
        self._dibujar_presupuesto_section(
            c, page_width, page_height, 
            y_start=page_height - 10*mm,  # Empezar más arriba
            y_end=mitad_altura + 5*mm,
            tipo="ORIGINAL",
            business_name=business_name,
            business_address=business_address,
            business_phone=business_phone,
            business_mobile=business_mobile,
            business_email=business_email,
            numero_presupuesto=reparacion['numero_presupuesto'],
            fecha_formateada=fecha_formateada,
            cliente_nombre=reparacion['cliente_nombre'],
            cliente_apellido=reparacion['cliente_apellido'],
            cliente_celular=reparacion['cliente_celular'],
            producto=reparacion['producto'],
            descripcion=reparacion.get('descripcion', ''),
            costo_reparacion=reparacion.get('costo_reparacion', 0),
            mostrar_costo=reparacion.get('costo_reparacion') is not None
        )
        
        # Línea separadora gruesa entre original y copia
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.line(15*mm, mitad_altura, page_width - 15*mm, mitad_altura)
        
        # Dibujar COPIA (mitad inferior) - más espacio hasta abajo
        self._dibujar_presupuesto_section(
            c, page_width, page_height,
            y_start=mitad_altura - 5*mm,
            y_end=10*mm,  # Terminar más abajo
            tipo="COPIA",
            business_name=business_name,
            business_address=business_address,
            business_phone=business_phone,
            business_mobile=business_mobile,
            business_email=business_email,
            numero_presupuesto=reparacion['numero_presupuesto'],
            fecha_formateada=fecha_formateada,
            cliente_nombre=reparacion['cliente_nombre'],
            cliente_apellido=reparacion['cliente_apellido'],
            cliente_celular=reparacion['cliente_celular'],
            producto=reparacion['producto'],
            descripcion=reparacion.get('descripcion', ''),
            costo_reparacion=reparacion.get('costo_reparacion', 0),
            mostrar_costo=reparacion.get('costo_reparacion') is not None
        )
        
        # Guardar PDF
        c.save()
        return pdf_path
    
    def _dibujar_presupuesto_section(self, canvas, page_width, page_height, y_start, y_end, tipo,
                                   business_name, business_address, business_phone, business_mobile, 
                                   business_email, numero_presupuesto, fecha_formateada,
                                   cliente_nombre, cliente_apellido, cliente_celular,
                                   producto, descripcion, costo_reparacion, mostrar_costo):
        """Dibujar sección del presupuesto con datos reales únicamente - diseño profesional"""
        
        # Márgenes y configuración
        margen_izq = 15*mm
        margen_der = page_width - 15*mm
        ancho_util = margen_der - margen_izq
        
        # Posición Y actual
        y_actual = y_start
        
        # Marco de la sección con bordes redondeados visual
        canvas.setStrokeColor(colors.Color(0.2, 0.2, 0.2))
        canvas.setLineWidth(1.2)
        canvas.rect(margen_izq, y_end, ancho_util, y_actual - y_end, fill=0, stroke=1)
        
        # Etiqueta ORIGINAL/COPIA en esquina superior derecha
        canvas.setFont("Helvetica-Bold", 12)
        canvas.setFillColor(colors.Color(0.1, 0.3, 0.6))
        canvas.drawRightString(margen_der - 3*mm, y_actual - 4*mm, tipo)
        
        y_actual -= 8*mm
        
        # === ENCABEZADO EMPRESARIAL ===
        # Fondo sutil para el encabezado
        canvas.setFillColor(colors.Color(0.96, 0.98, 1.0))
        canvas.rect(margen_izq + 1*mm, y_actual - 2*mm, ancho_util - 2*mm, 16*mm, fill=1, stroke=0)
        
        # Nombre del negocio destacado
        canvas.setFont("Helvetica-Bold", 16)
        canvas.setFillColor(colors.Color(0.1, 0.3, 0.6))
        business_width = canvas.stringWidth(business_name, "Helvetica-Bold", 16)
        canvas.drawString((page_width - business_width) / 2, y_actual, business_name)
        y_actual -= 6*mm
        
        # Información de contacto en líneas compactas
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(colors.Color(0.3, 0.3, 0.3))
        
        if business_address:
            addr_width = canvas.stringWidth(business_address, "Helvetica", 10)
            canvas.drawString((page_width - addr_width) / 2, y_actual, business_address)
            y_actual -= 4*mm
        
        # Teléfonos en una línea
        tel_info = []
        if business_phone:
            tel_info.append(f"Tel: {business_phone}")
        if business_mobile:
            tel_info.append(f"Cel: {business_mobile}")
        
        if tel_info:
            tel_text = " • ".join(tel_info)
            tel_width = canvas.stringWidth(tel_text, "Helvetica", 10)
            canvas.drawString((page_width - tel_width) / 2, y_actual, tel_text)
            y_actual -= 5*mm
        
        y_actual -= 4*mm
        
        # Línea separadora elegante
        canvas.setStrokeColor(colors.Color(0.1, 0.3, 0.6))
        canvas.setLineWidth(1)
        canvas.line(margen_izq + 15*mm, y_actual, margen_der - 15*mm, y_actual)
        y_actual -= 7*mm
        
        # === INFORMACIÓN DEL PRESUPUESTO ===
        canvas.setFont("Helvetica-Bold", 14)
        canvas.setFillColor(colors.Color(0.1, 0.3, 0.6))
        titulo_width = canvas.stringWidth("COMPROBANTE DE REPARACIÓN", "Helvetica-Bold", 14)
        canvas.drawString((page_width - titulo_width) / 2, y_actual, "COMPROBANTE DE REPARACIÓN")
        y_actual -= 7*mm
        
        # Número y fecha en dos columnas
        canvas.setFont("Helvetica-Bold", 11)
        canvas.setFillColor(colors.black)
        canvas.drawString(margen_izq + 3*mm, y_actual, f"N° {numero_presupuesto}")
        
        fecha_text = f"Fecha: {fecha_formateada}"
        fecha_width = canvas.stringWidth(fecha_text, "Helvetica-Bold", 11)
        canvas.drawString(margen_der - fecha_width - 3*mm, y_actual, fecha_text)
        y_actual -= 8*mm
        
        # === DATOS DEL CLIENTE ===
        # Fondo sutil para sección cliente
        cliente_height = 24*mm  # Aumentado para incluir más información
        canvas.setFillColor(colors.Color(0.98, 0.98, 0.98))
        canvas.rect(margen_izq + 1*mm, y_actual - cliente_height, ancho_util - 2*mm, cliente_height + 1*mm, fill=1, stroke=0)
        
        canvas.setFont("Helvetica-Bold", 12)
        canvas.setFillColor(colors.Color(0.1, 0.3, 0.6))
        canvas.drawString(margen_izq + 3*mm, y_actual, "CLIENTE")
        y_actual -= 6*mm
        
        # Datos del cliente en líneas compactas
        canvas.setFont("Helvetica", 11)
        canvas.setFillColor(colors.black)
        
        cliente_completo = f"{cliente_nombre} {cliente_apellido}"
        canvas.drawString(margen_izq + 3*mm, y_actual, f"Nombre: {cliente_completo}")
        y_actual -= 5*mm
        
        if cliente_celular:
            canvas.drawString(margen_izq + 3*mm, y_actual, f"Teléfono: {cliente_celular}")
            y_actual -= 5*mm
        
        # Información del equipo y trabajo
        canvas.drawString(margen_izq + 3*mm, y_actual, f"Equipo: {producto}")
        y_actual -= 5*mm
        
        # Descripción del trabajo con formato mejorado
        if descripcion:
            # Dividir descripción en líneas si es necesario
            max_width = ancho_util - 6*mm
            palabras = descripcion.split()
            lineas_desc = []
            linea_actual = ""
            
            for palabra in palabras:
                linea_test = linea_actual + " " + palabra if linea_actual else palabra
                if canvas.stringWidth(linea_test, "Helvetica", 11) <= max_width:
                    linea_actual = linea_test
                else:
                    if linea_actual:
                        lineas_desc.append(linea_actual)
                        linea_actual = palabra
                    else:
                        lineas_desc.append(palabra)
                        linea_actual = ""
            
            if linea_actual:
                lineas_desc.append(linea_actual)
            
            # Mostrar descripción
            for i, linea in enumerate(lineas_desc):
                prefijo = "Trabajo:" if i == 0 else "        "
                canvas.drawString(margen_izq + 3*mm, y_actual, f"{prefijo} {linea}")
                y_actual -= 5*mm
        
        y_actual -= 2*mm
        
        # === COSTO ===
        if mostrar_costo and costo_reparacion > 0:
            # Marco destacado para el costo
            canvas.setFillColor(colors.Color(0.95, 0.98, 1.0))
            canvas.setStrokeColor(colors.Color(0.1, 0.3, 0.6))
            canvas.setLineWidth(1.5)
            costo_height = 9*mm
            canvas.rect(margen_izq + 1*mm, y_actual - costo_height, ancho_util - 2*mm, costo_height, fill=1, stroke=1)
            
            canvas.setFont("Helvetica-Bold", 14)
            canvas.setFillColor(colors.Color(0.1, 0.3, 0.6))
            costo_text = f"COSTO ESTIMADO: ${costo_reparacion:,.2f}"
            costo_width = canvas.stringWidth(costo_text, "Helvetica-Bold", 14)
            canvas.drawString((page_width - costo_width) / 2, y_actual - 6*mm, costo_text)
            y_actual -= 11*mm
        
        # === FIRMA ===
        # Línea para firma
        firma_y = y_end + 18*mm  # Subir más la firma
        canvas.setStrokeColor(colors.Color(0.3, 0.3, 0.3))
        canvas.setLineWidth(1)
        canvas.line(margen_der - 80*mm, firma_y, margen_der - 3*mm, firma_y)
        
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.Color(0.5, 0.5, 0.5))
        canvas.drawString(margen_der - 60*mm, firma_y - 4*mm, "Firma y Aclaración del Cliente")
        
        # === CONDICIONES Y TÉRMINOS ===
        # Condiciones centradas por debajo de la firma con letra más pequeña
        canvas.setFont("Helvetica", 7)  # Letra más pequeña
        canvas.setFillColor(colors.Color(0.4, 0.4, 0.4))
        
        # Primera condición centrada
        condicion1 = "En caso de no aceptar el presupuesto se cobrará $10.000 por concepto de revisión"
        condicion1_width = canvas.stringWidth(condicion1, "Helvetica", 7)
        canvas.drawString((page_width - condicion1_width) / 2, firma_y - 10*mm, condicion1)
        
        # Segunda condición centrada
        condicion2 = "Si la reparación permanece más de 1 mes, el precio del presupuesto aumentará"
        condicion2_width = canvas.stringWidth(condicion2, "Helvetica", 7)
        canvas.drawString((page_width - condicion2_width) / 2, firma_y - 14*mm, condicion2)