import logging
import json
from datetime import datetime
from typing import Any, Dict, Optional

class StructuredLogger:
    """
    Logger estructurado para el sistema de scraping.
    Permite logging con metadatos adicionales en formato JSON.
    """
    
    def __init__(self, service: str = "trigger-causas"):
        self.service = service
        self.logger = logging.getLogger(service)
        
        # Configurar nivel de logging
        self.logger.setLevel(logging.INFO)
        
        # Evitar duplicación de handlers
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _log(self, level: str, message: str, **kwargs):
        """Método interno para logging estructurado"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "service": self.service,
            "level": level,
            "message": message,
            **kwargs
        }
        
        log_message = json.dumps(log_data, ensure_ascii=False)
        
        if level == "info":
            self.logger.info(log_message)
        elif level == "error":
            self.logger.error(log_message)
        elif level == "warning":
            self.logger.warning(log_message)
        elif level == "debug":
            self.logger.debug(log_message)
        else:
            self.logger.info(log_message)
    
    def info(self, message: str, **kwargs):
        """Log de información"""
        self._log("info", message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log de error"""
        self._log("error", message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log de advertencia"""
        self._log("warning", message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log de debug"""
        self._log("debug", message, **kwargs)
    
    def exception(self, message: str, **kwargs):
        """Log de excepción con traceback"""
        self._log("error", message, **kwargs) 
