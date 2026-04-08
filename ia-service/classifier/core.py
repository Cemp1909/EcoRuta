from enum import Enum
from typing import Dict, Optional

class CategoriaResiduo(str, Enum):
    RECICLABLE = "reciclable"
    REUTILIZABLE = "reutilizable"
    REPARABLE = "reparable"
    PELIGROSO = "peligroso"
    ORGANICO = "organico"

class AccionRecomendada(str, Enum):
    RECICLAR = "reciclar"
    DONAR = "donar"
    REPARAR = "reparar"
    DISPOSICION_ESPECIAL = "disposicion_especial"
    COMPOSTAR = "compostar"

class ClasificadorAvanzado:
    def clasificar(self, nombre: str, material: str = None,
                   estado: str = None, electronico: bool = False,
                   contiene_baterias: bool = False) -> Dict:
        
        nombre_lower = nombre.lower()
        
        # Reglas de clasificación
        if contiene_baterias:
            return {
                "categoria": CategoriaResiduo.PELIGROSO,
                "accion": AccionRecomendada.DISPOSICION_ESPECIAL,
                "instrucciones": "⚠️ Contiene baterías - llevar a punto limpio",
                "confianza": 0.95,
                "factores": ["baterías detectadas"]
            }
        
        if electronico:
            return {
                "categoria": CategoriaResiduo.REPARABLE,
                "accion": AccionRecomendada.REPARAR,
                "instrucciones": "📱 Dispositivo electrónico - intentar reparar",
                "confianza": 0.85,
                "factores": ["electrónico"]
            }
        
        # Palabras clave
        if any(word in nombre_lower for word in ["plastico", "botella", "envase"]):
            return {
                "categoria": CategoriaResiduo.RECICLABLE,
                "accion": AccionRecomendada.RECICLAR,
                "instrucciones": "♻️ Depositar en contenedor amarillo",
                "confianza": 0.9,
                "factores": ["material plástico"]
            }
        
        if any(word in nombre_lower for word in ["vidrio", "frasco", "botella vidrio"]):
            return {
                "categoria": CategoriaResiduo.RECICLABLE,
                "accion": AccionRecomendada.RECICLAR,
                "instrucciones": "🥤 Depositar en contenedor verde",
                "confianza": 0.9,
                "factores": ["vidrio"]
            }
        
        if any(word in nombre_lower for word in ["papel", "carton", "caja"]):
            return {
                "categoria": CategoriaResiduo.RECICLABLE,
                "accion": AccionRecomendada.RECICLAR,
                "instrucciones": "📦 Depositar en contenedor azul",
                "confianza": 0.9,
                "factores": ["papel/cartón"]
            }
        
        if any(word in nombre_lower for word in ["ropa", "zapato", "vestido", "pantalon"]):
            return {
                "categoria": CategoriaResiduo.REUTILIZABLE,
                "accion": AccionRecomendada.DONAR,
                "instrucciones": "👕 Donar si está en buen estado",
                "confianza": 0.85,
                "factores": ["textil"]
            }
        
        if any(word in nombre_lower for word in ["comida", "resto", "cascara", "organico"]):
            return {
                "categoria": CategoriaResiduo.ORGANICO,
                "accion": AccionRecomendada.COMPOSTAR,
                "instrucciones": "🌱 Residuo orgánico - compostar",
                "confianza": 0.9,
                "factores": ["orgánico"]
            }
        
        # Default
        return {
            "categoria": CategoriaResiduo.RECICLABLE,
            "accion": AccionRecomendada.RECICLAR,
            "instrucciones": "♻️ Reciclar según normativa local",
            "confianza": 0.6,
            "factores": ["clasificación genérica"]
        }
