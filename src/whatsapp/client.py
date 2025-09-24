"""
Cliente para WhatsApp Web
Abre WhatsApp Web con mensajes pre-escritos listos para enviar
"""

import webbrowser
import urllib.parse
import logging
import os
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class WhatsAppClient:
    """Cliente para integración con WhatsApp Web"""
    
    def __init__(self):
        """Inicializar el cliente de WhatsApp"""
        self.business_name = os.getenv('BUSINESS_NAME', 'InstaFix')
        self.business_slogan = os.getenv('BUSINESS_SLOGAN', '')
        self.business_hours = os.getenv('BUSINESS_HOURS', 'Lunes a Viernes 9:00-18:00')
        self.business_address = os.getenv('BUSINESS_ADDRESS', '')
        self.business_phone = os.getenv('BUSINESS_PHONE', '')
        self.business_mobile = os.getenv('BUSINESS_MOBILE', '')
        self.business_email = os.getenv('BUSINESS_EMAIL', '')
        self.business_extra = os.getenv('BUSINESS_EXTRA', '')
        self.enabled = True  # WhatsApp Web siempre está disponible
        logger.info("Cliente WhatsApp Web inicializado correctamente")
    
    def _send_message_whatsapp_web(self, to: str, message: str) -> bool:
        """
        Abrir WhatsApp Web con mensaje pre-escrito
        
        Args:
            to (str): Número de teléfono (formato internacional)
            message (str): Mensaje a enviar
            
        Returns:
            bool: True si se abrió correctamente
        """
        # Limpiar y formatear número
        phone_number = self._clean_phone_number(to)
        if not phone_number:
            logger.error(f"Número de teléfono inválido: {to}")
            return False
        
        # Codificar mensaje para URL
        encoded_message = urllib.parse.quote(message)
        
        # Crear URL de WhatsApp Web
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
        
        try:
            # Abrir en el navegador predeterminado
            webbrowser.open(whatsapp_url)
            logger.info(f"WhatsApp Web abierto para {phone_number}")
            return True
            
        except Exception as e:
            logger.error(f"Error al abrir WhatsApp Web: {e}")
            return False
    
    def _clean_phone_number(self, phone: str) -> Optional[str]:
        """
        Limpiar y formatear número de teléfono
        
        Args:
            phone (str): Número de teléfono
            
        Returns:
            Optional[str]: Número limpio o None si es inválido
        """
        if not phone:
            return None
        
        # Remover espacios, guiones y paréntesis
        phone = ''.join(filter(str.isdigit, phone))
        
        # Si no tiene código de país, agregar 54 (Argentina)
        if len(phone) == 10 and phone.startswith('11'):
            phone = '54' + phone
        elif len(phone) == 10:
            phone = '549' + phone
        elif len(phone) == 11 and not phone.startswith('54'):
            phone = '54' + phone[1:]  # Remover el 0 inicial
        
        # Validar longitud
        if len(phone) < 10 or len(phone) > 15:
            return None
        
        return phone
    
    def enviar_notificacion_costo(self, cliente_nombre: str, cliente_apellido: str, 
                                 celular: str, producto: str, costo: float, 
                                 descripcion: str = "") -> bool:
        """
        Abrir WhatsApp Web con notificación de costo pre-escrita
        
        Args:
            cliente_nombre (str): Nombre del cliente
            cliente_apellido (str): Apellido del cliente
            celular (str): Número de celular
            producto (str): Producto a reparar
            costo (float): Costo de la reparación
            descripcion (str): Descripción opcional
            
        Returns:
            bool: True si se abrió WhatsApp Web correctamente
        """
        mensaje = self._generar_mensaje_costo(
            cliente_nombre, cliente_apellido, producto, costo, descripcion
        )
        
        return self._send_message_whatsapp_web(celular, mensaje)
    
    def enviar_notificacion_finalizado(self, cliente_nombre: str, cliente_apellido: str, 
                                     celular: str, producto: str) -> bool:
        """
        Abrir WhatsApp Web con notificación de reparación finalizada pre-escrita
        
        Args:
            cliente_nombre (str): Nombre del cliente
            cliente_apellido (str): Apellido del cliente
            celular (str): Número de celular
            producto (str): Producto reparado
            
        Returns:
            bool: True si se abrió WhatsApp Web correctamente
        """
        mensaje = self._generar_mensaje_finalizado(
            cliente_nombre, cliente_apellido, producto
        )
        
        return self._send_message_whatsapp_web(celular, mensaje)
    
    def enviar_notificacion_retirado(self, cliente_nombre: str, cliente_apellido: str, 
                                   celular: str, producto: str) -> bool:
        """
        Abrir WhatsApp Web con notificación de confirmación de retiro pre-escrita
        
        Args:
            cliente_nombre (str): Nombre del cliente
            cliente_apellido (str): Apellido del cliente
            celular (str): Número de celular
            producto (str): Producto retirado
            
        Returns:
            bool: True si se abrió WhatsApp Web correctamente
        """
        mensaje = self._generar_mensaje_retirado(
            cliente_nombre, cliente_apellido, producto
        )
        
        return self._send_message_whatsapp_web(celular, mensaje)
    
    def enviar_mensaje_personalizado(self, celular: str, mensaje: str) -> bool:
        """
        Abrir WhatsApp Web con mensaje personalizado pre-escrito
        
        Args:
            celular (str): Número de celular
            mensaje (str): Mensaje personalizado
            
        Returns:
            bool: True si se abrió WhatsApp Web correctamente
        """
        return self._send_message_whatsapp_web(celular, mensaje)
    
    def _generar_mensaje_costo(self, nombre: str, apellido: str, producto: str, 
                              costo: float, descripcion: str = "") -> str:
        """Generar mensaje de notificación de costo"""
        mensaje = f"🔧 *{self.business_name}*"
        if self.business_slogan:
            mensaje += f"\n_{self.business_slogan}_"
        mensaje += "\n\n"
        
        mensaje += f"Hola {nombre} {apellido}!\n\n"
        mensaje += f"Te informamos que hemos evaluado tu *{producto}*.\n\n"
        
        if descripcion:
            mensaje += f"� *Información sobre la reparación:* {descripcion}\n\n"
        
        mensaje += f"💰 *Costo de reparación:* ${costo:,.2f}\n\n"
        
        # Información de contacto y horarios
        mensaje += "📞 *Información de contacto:*\n"
        mensaje += f"⏰ *Horarios:* {self.business_hours}\n"
        
        if self.business_mobile:
            mensaje += f"📱 *WhatsApp:* {self.business_mobile}\n"
        if self.business_phone:
            mensaje += f"☎️ *Teléfono:* {self.business_phone}\n"
        if self.business_address:
            mensaje += f"📍 *Dirección:* {self.business_address}\n"
        
        mensaje += "\nPor favor, confirma si deseas proceder con la reparación.\n\n"
        
        if self.business_extra:
            mensaje += f"ℹ️ {self.business_extra}\n\n"
        
        mensaje += "¡Gracias por confiar en nosotros! 🙂"
        
        return mensaje
    
    def _generar_mensaje_finalizado(self, nombre: str, apellido: str, producto: str) -> str:
        """Generar mensaje de reparación finalizada"""
        mensaje = f"✅ *{self.business_name}*"
        if self.business_slogan:
            mensaje += f"\n_{self.business_slogan}_"
        mensaje += "\n\n"
        
        mensaje += f"¡Excelente noticia {nombre} {apellido}!\n\n"
        mensaje += f"Tu *{producto}* ya está listo para retirar. 🎉\n\n"
        
        # Información de contacto y horarios
        mensaje += "📞 *Información para el retiro:*\n"
        mensaje += f"⏰ *Horarios:* {self.business_hours}\n"
        
        if self.business_mobile:
            mensaje += f"📱 *WhatsApp:* {self.business_mobile}\n"
        if self.business_phone:
            mensaje += f"☎️ *Teléfono:* {self.business_phone}\n"
        if self.business_address:
            mensaje += f"📍 *Dirección:* {self.business_address}\n"
        
        mensaje += "\nTe esperamos para la entrega.\n\n"
        
        if self.business_extra:
            mensaje += f"ℹ️ {self.business_extra}\n\n"
            
        mensaje += "¡Gracias por tu paciencia! 😊"
        
        return mensaje
    
    def _generar_mensaje_retirado(self, nombre: str, apellido: str, producto: str) -> str:
        """Generar mensaje de confirmación de retiro"""
        mensaje = f"✅ *{self.business_name}*"
        if self.business_slogan:
            mensaje += f"\n_{self.business_slogan}_"
        mensaje += "\n\n"
        
        mensaje += f"Confirmamos que {nombre} {apellido} retiró su *{producto}*.\n\n"
        mensaje += "¡Esperamos que todo funcione perfectamente!\n\n"
        
        mensaje += "📞 *Mantente en contacto:*\n"
        if self.business_mobile:
            mensaje += f"📱 *WhatsApp:* {self.business_mobile}\n"
        if self.business_phone:
            mensaje += f"☎️ *Teléfono:* {self.business_phone}\n"
        if self.business_email:
            mensaje += f"📧 *Email:* {self.business_email}\n"
            
        mensaje += "\nSi tienes algún inconveniente, no dudes en contactarnos.\n\n"
        
        if self.business_extra:
            mensaje += f"ℹ️ {self.business_extra}\n\n"
            
        mensaje += "¡Gracias por elegirnos! 🙂"
        
        return mensaje
    
    def test_connection(self) -> bool:
        """
        Probar que se puede abrir WhatsApp Web
        
        Returns:
            bool: True si WhatsApp Web está disponible
        """
        try:
            # Probar abriendo WhatsApp Web sin número específico
            test_url = "https://web.whatsapp.com"
            webbrowser.open(test_url)
            logger.info("WhatsApp Web abierto correctamente")
            return True
            
        except Exception as e:
            logger.error(f"Error al abrir WhatsApp Web: {e}")
            return False