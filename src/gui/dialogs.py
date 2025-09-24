"""
Diálogos personalizados para InstaFix
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict
import os
import re

def maximize_window(window):
    """
    Función auxiliar para maximizar una ventana de forma multiplataforma
    
    Args:
        window: Ventana de Tkinter a maximizar
    """
    # Asegurar que la ventana esté completamente inicializada
    window.update_idletasks()
    
    # Para diálogos (Toplevel), usar una aproximación más directa
    if isinstance(window, tk.Toplevel):
        # Obtener dimensiones de la pantalla
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # En macOS, restar un poco para la barra de menú y dock
        if hasattr(window, 'tk') and window.tk.call('tk', 'windowingsystem') == 'aqua':
            screen_height -= 25  # Barra de menú
        
        # Establecer geometría para ocupar toda la pantalla
        window.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Intentar también maximizar si es posible
        window.after(100, lambda: try_maximize(window))
    else:
        # Para la ventana principal, usar los métodos estándar
        try_maximize(window)

def try_maximize(window):
    """Intentar maximizar usando métodos específicos del sistema"""
    try:
        # Para macOS
        window.attributes('-zoomed', True)
    except tk.TclError:
        try:
            # Para Windows/Linux
            window.state('zoomed')
        except tk.TclError:
            pass  # Ya se estableció la geometría manualmente

class ReparacionDialog:
    """Diálogo para crear/editar reparaciones"""
    
    def __init__(self, parent, title: str, reparacion: Optional[Dict] = None):
        """
        Inicializar diálogo de reparación
        
        Args:
            parent: Ventana padre
            title (str): Título del diálogo
            reparacion (Optional[Dict]): Datos de reparación existente para editar
        """
        self.parent = parent
        self.result = None
        self.reparacion = reparacion
        
        # Crear ventana
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.resizable(True, True)  # Permitir redimensionar si es necesario
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Crear interfaz primero
        self._create_widgets()
        
        # Maximizar ventana después de crear widgets
        self._center_window()
        
        # Si es edición, cargar datos
        if reparacion:
            self._load_data()
        
        # Foco inicial
        self.cliente_nombre_entry.focus_set()
        
        # Esperar resultado
        self.dialog.wait_window()
    
    def _center_window(self):
        """Maximizar ventana del diálogo"""
        maximize_window(self.dialog)
    
    def _create_widgets(self):
        """Crear widgets del diálogo"""
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="📋 Datos de la Reparación", 
                              font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Frame de datos del cliente
        cliente_frame = ttk.LabelFrame(main_frame, text="👤 Datos del Cliente", padding="15")
        cliente_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Configurar grid para aprovechamiento completo del ancho
        cliente_frame.columnconfigure(1, weight=1)
        cliente_frame.columnconfigure(3, weight=1)
        cliente_frame.columnconfigure(5, weight=1)
        
        # Row 1: Nombre, Apellido, Celular (tres campos en una fila)
        ttk.Label(cliente_frame, text="Nombre:", font=('Arial', 11, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=10, padx=(0, 15))
        self.cliente_nombre_var = tk.StringVar()
        self.cliente_nombre_entry = ttk.Entry(cliente_frame, textvariable=self.cliente_nombre_var, 
                                            font=('Arial', 11))
        self.cliente_nombre_entry.grid(row=0, column=1, pady=10, padx=(0, 30), sticky=tk.EW)
        
        ttk.Label(cliente_frame, text="Apellido:", font=('Arial', 11, 'bold')).grid(
            row=0, column=2, sticky=tk.W, pady=10, padx=(0, 15))
        self.cliente_apellido_var = tk.StringVar()
        self.cliente_apellido_entry = ttk.Entry(cliente_frame, textvariable=self.cliente_apellido_var, 
                                              font=('Arial', 11))
        self.cliente_apellido_entry.grid(row=0, column=3, pady=10, padx=(0, 30), sticky=tk.EW)
        
        ttk.Label(cliente_frame, text="Celular:", font=('Arial', 11, 'bold')).grid(
            row=0, column=4, sticky=tk.W, pady=10, padx=(0, 15))
        self.cliente_celular_var = tk.StringVar()
        self.cliente_celular_entry = ttk.Entry(cliente_frame, textvariable=self.cliente_celular_var, 
                                             font=('Arial', 11))
        self.cliente_celular_entry.grid(row=0, column=5, pady=10, sticky=tk.EW)
        
        # Frame de datos de la reparación
        reparacion_frame = ttk.LabelFrame(main_frame, text="🔧 Datos de la Reparación", padding="15")
        reparacion_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Configurar grid para dos columnas principales
        reparacion_frame.columnconfigure(1, weight=1)
        reparacion_frame.columnconfigure(3, weight=1)
        
        # Row 1: Producto y Estado (lado a lado)
        ttk.Label(reparacion_frame, text="Producto:", font=('Arial', 11, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=10, padx=(0, 15))
        self.producto_var = tk.StringVar()
        self.producto_combo = ttk.Combobox(reparacion_frame, textvariable=self.producto_var, 
                                         font=('Arial', 11))
        self.producto_combo['values'] = [
            'PC de Escritorio', 'Notebook', 'Celular',
            'Impresora', 'Calculadora',
        ]
        self.producto_combo.grid(row=0, column=1, pady=10, padx=(0, 30), sticky=tk.EW)
        
        ttk.Label(reparacion_frame, text="Estado:", font=('Arial', 11, 'bold')).grid(
            row=0, column=2, sticky=tk.W, pady=10, padx=(0, 15))
        self.estado_var = tk.StringVar(value="pendiente")
        self.estado_combo = ttk.Combobox(reparacion_frame, textvariable=self.estado_var, 
                                       values=["pendiente", "en_proceso", "finalizado", "retirado"],
                                       state="readonly", font=('Arial', 11))
        self.estado_combo.grid(row=0, column=3, pady=10, sticky=tk.EW)
        
        # Row 2: Costo (ocupando menos espacio, centrado a la izquierda)
        ttk.Label(reparacion_frame, text="Costo ($):", font=('Arial', 11, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=10, padx=(0, 15))
        self.costo_var = tk.StringVar()
        self.costo_entry = ttk.Entry(reparacion_frame, textvariable=self.costo_var, 
                                   font=('Arial', 11), width=20)
        self.costo_entry.grid(row=1, column=1, pady=10, sticky=tk.W)
        
        # Row 3: Descripción técnica (ocupando todo el ancho)
        ttk.Label(reparacion_frame, text="Descripción Técnica:", font=('Arial', 11, 'bold')).grid(
            row=2, column=0, sticky=tk.NW, pady=(10, 5), padx=(0, 15))
        
        # Frame para descripción con scrollbar
        desc_container = ttk.Frame(reparacion_frame)
        desc_container.grid(row=2, column=1, columnspan=3, pady=(10, 10), sticky=tk.EW)
        desc_container.columnconfigure(0, weight=1)
        
        self.descripcion_text = tk.Text(desc_container, height=4, wrap=tk.WORD,
                                      bg='white', fg='black', insertbackground='black',
                                      font=('Arial', 11), relief=tk.SOLID, borderwidth=1)
        self.descripcion_text.grid(row=0, column=0, sticky=tk.EW)
        
        # Scrollbar para descripción
        desc_scrollbar = ttk.Scrollbar(desc_container, orient=tk.VERTICAL, 
                                     command=self.descripcion_text.yview)
        desc_scrollbar.grid(row=0, column=1, sticky='ns')
        self.descripcion_text.configure(yscrollcommand=desc_scrollbar.set)
        
        # Frame de mensaje para cliente (WhatsApp)
        mensaje_frame = ttk.LabelFrame(main_frame, text="📱 Mensaje para Cliente (WhatsApp)", padding="15")
        mensaje_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Etiqueta informativa
        info_label = ttk.Label(mensaje_frame, 
                             text="💡 Este mensaje se enviará al cliente junto con el costo por WhatsApp (NO se envía la descripción técnica)",
                             font=('Arial', 10), foreground='#666666')
        info_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Frame para el texto con scrollbar
        notas_container = ttk.Frame(mensaje_frame)
        notas_container.pack(fill=tk.BOTH, expand=True)
        notas_container.columnconfigure(0, weight=1)
        
        self.notas_text = tk.Text(notas_container, height=4, wrap=tk.WORD,
                                bg='white', fg='black', insertbackground='black',
                                relief=tk.SOLID, borderwidth=1, font=('Arial', 11))
        self.notas_text.grid(row=0, column=0, sticky=tk.EW)
        
        # Scrollbar para notas
        notas_scrollbar = ttk.Scrollbar(notas_container, orient=tk.VERTICAL, 
                                      command=self.notas_text.yview)
        notas_scrollbar.grid(row=0, column=1, sticky='ns')
        self.notas_text.configure(yscrollcommand=notas_scrollbar.set)
        
        # Placeholder text
        placeholder_text = "Ejemplo: 'Se realizó limpieza completa del sistema, cambio de pasta térmica y actualización del sistema operativo. El equipo quedó funcionando correctamente.'"
        self.notas_text.insert(1.0, placeholder_text)
        self.notas_text.config(fg='#999999')
        
        # Eventos para placeholder
        def on_focus_in(event):
            if self.notas_text.get(1.0, tk.END).strip() == placeholder_text:
                self.notas_text.delete(1.0, tk.END)
                self.notas_text.config(fg='black')
        
        def on_focus_out(event):
            if not self.notas_text.get(1.0, tk.END).strip():
                self.notas_text.insert(1.0, placeholder_text)
                self.notas_text.config(fg='#999999')
        
        self.notas_text.bind('<FocusIn>', on_focus_in)
        self.notas_text.bind('<FocusOut>', on_focus_out)
        
        # Agregar un separador visual antes de los botones
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(20, 10))
        
        # Botones - Frame con mejor estilo y más espacio
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(40, 20))  # Más padding arriba y abajo
        
        # Crear frame interno centrado para los botones
        buttons_inner = ttk.Frame(buttons_frame)
        buttons_inner.pack(expand=True)
        
        # Definir texto según si es nueva reparación o edición
        if self.reparacion:  # Es edición
            guardar_text = "✅ Confirmar Cambios"
        else:  # Es nueva reparación
            guardar_text = "✅ Crear Reparación"
        
        # Botón Cancelar - más grande y visible
        cancel_btn = ttk.Button(buttons_inner, text="❌ Cancelar", 
                               command=self._cancel, width=18)  # Más ancho
        cancel_btn.pack(side=tk.LEFT, padx=(0, 30), pady=10)  # Más separación
        
        # Botón Guardar - más grande y como botón principal
        save_btn = ttk.Button(buttons_inner, text=guardar_text, 
                             command=self._save, width=25)  # Más ancho
        save_btn.pack(side=tk.LEFT, pady=10)
        
        # Hacer que el botón Guardar sea el predeterminado
        save_btn.focus_set()
        
        # Validación de entrada para costo
        self.costo_entry.bind('<KeyRelease>', self._validate_cost)
        
        # Solo mantener Escape para cancelar - NO Enter automático
        self.dialog.bind('<Escape>', lambda e: self._cancel())
        
        # Permitir Enter solo en el botón de guardar cuando tiene foco
        def on_save_enter(event):
            if event.widget == save_btn:
                self._save()
        save_btn.bind('<Return>', on_save_enter)
    
    def _load_data(self):
        """Cargar datos de reparación existente"""
        if not self.reparacion:
            return
        
        # Cargar datos del cliente
        self.cliente_nombre_var.set(self.reparacion.get('cliente_nombre', ''))
        self.cliente_apellido_var.set(self.reparacion.get('cliente_apellido', ''))
        self.cliente_celular_var.set(self.reparacion.get('cliente_celular', ''))
        
        # Cargar datos de reparación
        self.producto_var.set(self.reparacion.get('producto', ''))
        
        # Descripción técnica
        if self.reparacion.get('descripcion'):
            self.descripcion_text.delete(1.0, tk.END)
            self.descripcion_text.insert(tk.END, self.reparacion['descripcion'])
        
        # Costo
        if self.reparacion.get('costo_reparacion'):
            self.costo_var.set(str(self.reparacion['costo_reparacion']))
        
        # Estado
        self.estado_var.set(self.reparacion.get('estado', 'pendiente'))
        
        # Mensaje para cliente
        if self.reparacion.get('notas'):
            self.notas_text.delete(1.0, tk.END)
            self.notas_text.insert(tk.END, self.reparacion['notas'])
            self.notas_text.config(fg='black')
    
    def _validate_cost(self, event=None):
        """Validar entrada de costo"""
        valor = self.costo_var.get()
        if valor and not re.match(r'^\d*\.?\d*$', valor):
            # Remover caracteres no válidos
            valor_limpio = re.sub(r'[^\d.]', '', valor)
            self.costo_var.set(valor_limpio)
    
    def _save(self):
        """Guardar datos"""
        # Validar campos obligatorios
        if not self.cliente_nombre_var.get().strip():
            messagebox.showerror("Error", "El nombre del cliente es obligatorio")
            self.cliente_nombre_entry.focus_set()
            return
        
        if not self.cliente_apellido_var.get().strip():
            messagebox.showerror("Error", "El apellido del cliente es obligatorio")
            self.cliente_apellido_entry.focus_set()
            return
        
        if not self.cliente_celular_var.get().strip():
            messagebox.showerror("Error", "El celular del cliente es obligatorio")
            self.cliente_celular_entry.focus_set()
            return
        
        if not self.producto_var.get().strip():
            messagebox.showerror("Error", "El producto es obligatorio")
            self.producto_combo.focus_set()
            return
        
        # Validar formato de celular
        celular = self.cliente_celular_var.get().strip()
        if not re.match(r'^[\d\s\-\(\)\+]*$', celular):
            messagebox.showerror("Error", "Formato de celular inválido")
            self.cliente_celular_entry.focus_set()
            return
        
        # Validar costo si se ingresó
        costo = None
        if self.costo_var.get().strip():
            try:
                costo = float(self.costo_var.get())
                if costo < 0:
                    messagebox.showerror("Error", "El costo no puede ser negativo")
                    self.costo_entry.focus_set()
                    return
            except ValueError:
                messagebox.showerror("Error", "Formato de costo inválido")
                self.costo_entry.focus_set()
                return
        
        # Obtener mensaje para cliente (sin placeholder)
        mensaje_cliente = self.notas_text.get(1.0, tk.END).strip()
        placeholder_text = "Ejemplo: 'Se realizó limpieza completa del sistema, cambio de pasta térmica y actualización del sistema operativo. El equipo quedó funcionando correctamente.'"
        if mensaje_cliente == placeholder_text:
            mensaje_cliente = ""
        
        # Crear diccionario de resultado
        self.result = {
            'cliente_nombre': self.cliente_nombre_var.get().strip(),
            'cliente_apellido': self.cliente_apellido_var.get().strip(),
            'cliente_celular': celular,
            'producto': self.producto_var.get().strip(),
            'descripcion': self.descripcion_text.get(1.0, tk.END).strip(),
            'costo_reparacion': costo,
            'estado': self.estado_var.get(),
            'notas': mensaje_cliente
        }
        
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancelar diálogo"""
        self.result = None
        self.dialog.destroy()


class WhatsAppDialog:
    """Diálogo para enviar mensajes por WhatsApp"""
    
    def __init__(self, parent, reparacion: Dict):
        """
        Inicializar diálogo de WhatsApp
        
        Args:
            parent: Ventana padre
            reparacion (Dict): Datos de la reparación
        """
        self.parent = parent
        self.reparacion = reparacion
        self.result = None
        
        # Crear ventana
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("📱 Enviar por WhatsApp")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Maximizar ventana
        self._center_window()
        
        # Crear interfaz
        self._create_widgets()
        
        # Esperar resultado
        self.dialog.wait_window()
    
    def _center_window(self):
        """Maximizar ventana del diálogo"""
        maximize_window(self.dialog)
    
    def _create_widgets(self):
        """Crear widgets del diálogo"""
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="📱 Enviar mensaje por WhatsApp", 
                              font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Información del cliente
        info_frame = ttk.LabelFrame(main_frame, text="👤 Cliente", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        cliente_text = f"{self.reparacion['cliente_nombre']} {self.reparacion['cliente_apellido']}"
        ttk.Label(info_frame, text=f"Nombre: {cliente_text}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Celular: {self.reparacion['cliente_celular']}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Producto: {self.reparacion['producto']}").pack(anchor=tk.W)
        
        # Tipo de mensaje
        tipo_frame = ttk.LabelFrame(main_frame, text="✉️ Tipo de Mensaje", padding="10")
        tipo_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.tipo_mensaje = tk.StringVar(value="costo")
        
        ttk.Radiobutton(tipo_frame, text="💰 Notificar Costo", 
                       variable=self.tipo_mensaje, value="costo").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(tipo_frame, text="✅ Notificar Finalizado", 
                       variable=self.tipo_mensaje, value="finalizado").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(tipo_frame, text="✏️ Mensaje Personalizado", 
                       variable=self.tipo_mensaje, value="personalizado").pack(anchor=tk.W, pady=2)
        
        # Mensaje personalizado (inicialmente oculto)
        self.mensaje_frame = ttk.LabelFrame(main_frame, text="✏️ Mensaje Personalizado", padding="10")
        
        self.mensaje_text = tk.Text(self.mensaje_frame, width=50, height=6, wrap=tk.WORD)
        self.mensaje_text.pack(fill=tk.BOTH, expand=True)
        
        # Evento para mostrar/ocultar mensaje personalizado
        self.tipo_mensaje.trace('w', self._toggle_mensaje_personalizado)
        
        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(buttons_frame, text="❌ Cancelar", command=self._cancel).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(buttons_frame, text="📱 Abrir WhatsApp Web", command=self._send).pack(side=tk.RIGHT)
    
    def _toggle_mensaje_personalizado(self, *args):
        """Mostrar/ocultar campo de mensaje personalizado"""
        if self.tipo_mensaje.get() == "personalizado":
            self.mensaje_frame.pack(fill=tk.X, pady=(0, 10), before=self.dialog.children['!frame'].children['!frame3'])
        else:
            self.mensaje_frame.pack_forget()
    
    def _send(self):
        """Enviar mensaje"""
        tipo = self.tipo_mensaje.get()
        
        if tipo == "personalizado":
            mensaje = self.mensaje_text.get(1.0, tk.END).strip()
            if not mensaje:
                messagebox.showerror("Error", "El mensaje personalizado no puede estar vacío")
                return
        else:
            mensaje = None
        
        self.result = {
            'tipo': tipo,
            'mensaje': mensaje
        }
        
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancelar diálogo"""
        self.result = None
        self.dialog.destroy()


class ConfigDialog:
    """Diálogo de configuración del negocio"""
    
    def __init__(self, parent):
        """
        Inicializar diálogo de configuración
        
        Args:
            parent: Ventana padre
        """
        self.parent = parent
        self.result = None
        
        # Crear ventana
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("⚙️ Configuración del Negocio")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Maximizar ventana
        self._center_window()
        
        # Crear interfaz
        self._create_widgets()
        
        # Cargar configuración actual
        self._load_current_config()
        
        # Esperar resultado
        self.dialog.wait_window()
    
    def _center_window(self):
        """Maximizar ventana del diálogo"""
        maximize_window(self.dialog)
    
    def _create_widgets(self):
        """Crear widgets del diálogo"""
        # Frame principal que ocupa toda la pantalla (similar a ReparacionDialog)
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título principal
        title_label = ttk.Label(main_frame, text="⚙️ Configuración del Negocio", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # === SECCIÓN 1: INFORMACIÓN BÁSICA ===
        basic_section = ttk.LabelFrame(main_frame, text="🏢 Información Básica", padding="15")
        basic_section.pack(fill=tk.X, pady=(0, 15))
        basic_section.columnconfigure(1, weight=1)
        basic_section.columnconfigure(3, weight=1)
        
        # Row 1: Nombre del negocio y Slogan (lado a lado)
        ttk.Label(basic_section, text="Nombre del Negocio:", font=('Arial', 11, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=10, padx=(0, 15))
        self.business_name_var = tk.StringVar()
        self.business_name_entry = ttk.Entry(basic_section, textvariable=self.business_name_var, 
                                           font=('Arial', 11))
        self.business_name_entry.grid(row=0, column=1, pady=10, padx=(0, 30), sticky=tk.EW)
        
        ttk.Label(basic_section, text="Slogan/Descripción:", font=('Arial', 11, 'bold')).grid(
            row=0, column=2, sticky=tk.W, pady=10, padx=(0, 15))
        self.business_slogan_var = tk.StringVar()
        self.business_slogan_entry = ttk.Entry(basic_section, textvariable=self.business_slogan_var, 
                                             font=('Arial', 11))
        self.business_slogan_entry.grid(row=0, column=3, pady=10, sticky=tk.EW)
        
        # === SECCIÓN 2: INFORMACIÓN DE CONTACTO ===
        contact_section = ttk.LabelFrame(main_frame, text="📞 Información de Contacto", padding="15")
        contact_section.pack(fill=tk.X, pady=(0, 15))
        contact_section.columnconfigure(1, weight=1)
        contact_section.columnconfigure(3, weight=1)
        
        # Row 1: Teléfono fijo y Celular
        ttk.Label(contact_section, text="Teléfono Fijo:", font=('Arial', 11, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=10, padx=(0, 15))
        self.business_phone_var = tk.StringVar()
        self.business_phone_entry = ttk.Entry(contact_section, textvariable=self.business_phone_var, 
                                            font=('Arial', 11))
        self.business_phone_entry.grid(row=0, column=1, pady=10, padx=(0, 30), sticky=tk.EW)
        
        ttk.Label(contact_section, text="Celular/WhatsApp:", font=('Arial', 11, 'bold')).grid(
            row=0, column=2, sticky=tk.W, pady=10, padx=(0, 15))
        self.business_mobile_var = tk.StringVar()
        self.business_mobile_entry = ttk.Entry(contact_section, textvariable=self.business_mobile_var, 
                                             font=('Arial', 11))
        self.business_mobile_entry.grid(row=0, column=3, pady=10, sticky=tk.EW)
        
        # Row 2: Email (ocupando todo el ancho)
        ttk.Label(contact_section, text="Email:", font=('Arial', 11, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=10, padx=(0, 15))
        self.business_email_var = tk.StringVar()
        self.business_email_entry = ttk.Entry(contact_section, textvariable=self.business_email_var, 
                                            font=('Arial', 11))
        self.business_email_entry.grid(row=1, column=1, columnspan=3, pady=10, sticky=tk.EW)
        
        # === SECCIÓN 3: UBICACIÓN Y HORARIOS ===
        location_section = ttk.LabelFrame(main_frame, text="📍 Ubicación y Horarios", padding="15")
        location_section.pack(fill=tk.X, pady=(0, 15))
        location_section.columnconfigure(1, weight=1)
        location_section.columnconfigure(3, weight=1)
        
        # Dirección
        ttk.Label(location_section, text="Dirección:", font=('Arial', 11, 'bold')).grid(
            row=0, column=0, sticky=tk.NW, pady=10, padx=(0, 15))
        self.business_address_text = tk.Text(location_section, width=40, height=3, wrap=tk.WORD,
                                           bg='white', fg='black', insertbackground='black', 
                                           font=('Arial', 11), relief=tk.SOLID, borderwidth=1)
        self.business_address_text.grid(row=0, column=1, pady=10, padx=(0, 30), sticky=tk.EW)
        
        # Horarios
        ttk.Label(location_section, text="Horarios:", font=('Arial', 11, 'bold')).grid(
            row=0, column=2, sticky=tk.NW, pady=10, padx=(0, 15))
        self.business_hours_text = tk.Text(location_section, width=40, height=3, wrap=tk.WORD,
                                         bg='white', fg='black', insertbackground='black', 
                                         font=('Arial', 11), relief=tk.SOLID, borderwidth=1)
        self.business_hours_text.grid(row=0, column=3, pady=10, sticky=tk.EW)
        
        # Placeholder para horarios  
        horarios_placeholder = "Ejemplo:\nLunes a Viernes: 9:00 - 18:00\nSábados: 9:00 - 14:00"
        self.business_hours_text.insert(1.0, horarios_placeholder)
        self.business_hours_text.config(fg='#999999')
        
        # Eventos para placeholder de horarios
        def on_hours_focus_in(event):
            if self.business_hours_text.get(1.0, tk.END).strip() == horarios_placeholder:
                self.business_hours_text.delete(1.0, tk.END)
                self.business_hours_text.config(fg='black')
        
        def on_hours_focus_out(event):
            if not self.business_hours_text.get(1.0, tk.END).strip():
                self.business_hours_text.insert(1.0, horarios_placeholder)
                self.business_hours_text.config(fg='#999999')
        
        self.business_hours_text.bind('<FocusIn>', on_hours_focus_in)
        self.business_hours_text.bind('<FocusOut>', on_hours_focus_out)
        
        # === INFORMACIÓN ADICIONAL ===
        info_section = ttk.LabelFrame(main_frame, text="💡 Información", padding="15")
        info_section.pack(fill=tk.X, pady=(0, 20))
        
        info_text = ttk.Label(info_section, 
                            text="Esta información se incluirá automáticamente en los mensajes de WhatsApp\n"
                                 "para dar una imagen más profesional a tu negocio.\n"
                                 "Todos los campos son opcionales excepto el nombre del negocio.",
                            font=('Arial', 10), foreground='#555555', justify=tk.CENTER)
        info_text.pack(pady=10)
        
        # === SEPARADOR Y BOTONES (similar a ReparacionDialog) ===
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(20, 10))
        
        # Frame de botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(20, 10))
        
        # Frame interno centrado para los botones
        buttons_inner = ttk.Frame(buttons_frame)
        buttons_inner.pack(expand=True)
        
        # Botones con el mismo estilo que ReparacionDialog
        cancel_btn = ttk.Button(buttons_inner, text="❌ Cancelar", 
                               command=self._cancel, width=18)
        cancel_btn.pack(side=tk.LEFT, padx=(0, 30), pady=10)
        
        save_btn = ttk.Button(buttons_inner, text="✅ Guardar Configuración", 
                             command=self._save, width=25)
        save_btn.pack(side=tk.LEFT, pady=10)
        
        # Hacer que el botón Guardar sea el predeterminado
        save_btn.focus_set()
        
        # Configurar teclas de acceso rápido
        self.dialog.bind('<Escape>', lambda e: self._cancel())
        
        def on_save_enter(event):
            if event.widget == save_btn:
                self._save()
        save_btn.bind('<Return>', on_save_enter)
    
    def _load_current_config(self):
        """Cargar configuración actual desde variables de entorno"""
        self.business_name_var.set(os.getenv('BUSINESS_NAME', 'InstaFix'))
        self.business_slogan_var.set(os.getenv('BUSINESS_SLOGAN', ''))
        self.business_phone_var.set(os.getenv('BUSINESS_PHONE', ''))
        self.business_mobile_var.set(os.getenv('BUSINESS_MOBILE', ''))
        self.business_email_var.set(os.getenv('BUSINESS_EMAIL', ''))
        
        # Dirección
        address = os.getenv('BUSINESS_ADDRESS', '')
        if address:
            self.business_address_text.delete(1.0, tk.END)
            self.business_address_text.insert(1.0, address)
        
        # Horarios
        hours = os.getenv('BUSINESS_HOURS', '')
        if hours:
            self.business_hours_text.delete(1.0, tk.END)
            self.business_hours_text.insert(1.0, hours)
            self.business_hours_text.config(fg='black')
    
    def _save(self):
        """Guardar configuración"""
        # Validar campos obligatorios
        if not self.business_name_var.get().strip():
            messagebox.showerror("Error", "El nombre del negocio es obligatorio")
            self.business_name_entry.focus_set()
            return
        
        # Obtener horarios sin placeholder
        horarios_placeholder = "Ejemplo:\nLunes a Viernes: 9:00 - 18:00\nSábados: 9:00 - 14:00\nDomingos: Cerrado"
        horarios_text = self.business_hours_text.get(1.0, tk.END).strip()
        if horarios_text == horarios_placeholder:
            horarios_text = "Lunes a Viernes 9:00-18:00"
        
        self.result = {
            'business_name': self.business_name_var.get().strip(),
            'business_slogan': self.business_slogan_var.get().strip(),
            'business_phone': self.business_phone_var.get().strip(),
            'business_mobile': self.business_mobile_var.get().strip(),
            'business_email': self.business_email_var.get().strip(),
            'business_address': self.business_address_text.get(1.0, tk.END).strip(),
            'business_hours': horarios_text
        }
        
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancelar diálogo"""
        self.result = None
        self.dialog.destroy()