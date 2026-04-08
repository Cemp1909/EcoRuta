from typing import Dict

class ClasificadorVision:
    def __init__(self):
        print("✅ ClasificadorVision listo")
    
    def clasificar_desde_imagen(self, imagen_bytes: bytes) -> Dict:
        # Versión simple mientras implementamos la IA de visión
        return {
            'objeto_detectado': 'objeto',
            'categoria': 'reciclable',
            'accion': 'reciclar',
            'confianza': 0.7,
            'instrucciones': 'Clasificado como reciclable',
            'otras_posibilidades': []
        }
