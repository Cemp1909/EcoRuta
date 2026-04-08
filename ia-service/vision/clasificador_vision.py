from io import BytesIO
from pathlib import Path
from typing import Dict, List

from PIL import Image
from loguru import logger
import torch
from torchvision import models


class ClasificadorVision:
    def __init__(self):
        self._base_dir = Path(__file__).resolve().parent.parent
        self._cache_dir = self._base_dir / ".torch_cache"
        self._custom_model_path = self._base_dir / "vision" / "modelo_residuos.pth"
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._model = None
        self._preprocess = None
        self._modelo_disponible = False
        self._usa_modelo_personalizado = False
        self._custom_classes: List[str] = []
        self._labels = self._cargar_labels_imagenet()
        self._inicializar_modelo()

    def _cargar_labels_imagenet(self) -> List[str]:
        labels_path = self._base_dir / "imagenet_classes.txt"
        with labels_path.open(encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def _crear_modelo_base(self):
        weights = models.MobileNet_V3_Small_Weights.DEFAULT
        model = models.mobilenet_v3_small(weights=weights)
        preprocess = weights.transforms()
        return model, preprocess

    def _crear_modelo_personalizado(self, num_classes: int):
        weights = models.MobileNet_V3_Small_Weights.DEFAULT
        model = models.mobilenet_v3_small(weights=weights)
        in_features = model.classifier[3].in_features
        model.classifier[3] = torch.nn.Linear(in_features, num_classes)
        preprocess = weights.transforms()
        return model, preprocess

    def _inicializar_modelo(self) -> None:
        try:
            self._cache_dir.mkdir(parents=True, exist_ok=True)
            torch.hub.set_dir(str(self._cache_dir))

            if self._custom_model_path.exists():
                checkpoint = torch.load(
                    self._custom_model_path,
                    map_location=self._device,
                )
                classes = checkpoint.get("classes", [])
                if not classes:
                    raise ValueError("El modelo personalizado no incluye la lista de clases.")

                self._custom_classes = list(classes)
                self._model, self._preprocess = self._crear_modelo_personalizado(
                    len(self._custom_classes)
                )
                self._model.load_state_dict(checkpoint["model_state"])
                self._usa_modelo_personalizado = True
                logger.info(f"ClasificadorVision cargado con modelo personalizado: {self._custom_model_path}")
            else:
                self._model, self._preprocess = self._crear_modelo_base()
                self._usa_modelo_personalizado = False
                logger.info("ClasificadorVision cargado con MobileNetV3 base")

            self._model = self._model.to(self._device)
            self._model.eval()
            self._modelo_disponible = True
        except Exception as e:
            self._modelo_disponible = False
            logger.exception(f"No se pudo cargar el modelo de vision: {e}")

    def clasificar_desde_imagen(self, imagen_bytes: bytes) -> Dict:
        if not self._modelo_disponible or self._model is None or self._preprocess is None:
            return {
                "objeto_detectado": "modelo_no_disponible",
                "categoria": "indeterminado",
                "accion": "revision_manual",
                "confianza": 0.0,
                "instrucciones": "No fue posible cargar el modelo de vision.",
                "otras_posibilidades": [],
            }

        image = Image.open(BytesIO(imagen_bytes)).convert("RGB")
        input_tensor = self._preprocess(image).unsqueeze(0).to(self._device)

        with torch.inference_mode():
            outputs = self._model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            top_k = min(5, probabilities.shape[0])
            top_probs, top_indices = torch.topk(probabilities, k=top_k)

        if self._usa_modelo_personalizado:
            predicciones = [
                {
                    "label": self._custom_classes[idx],
                    "confianza": float(prob),
                }
                for prob, idx in zip(top_probs.tolist(), top_indices.tolist())
            ]
            principal = predicciones[0]
            decision = self._mapear_clase_personalizada(principal["label"], principal["confianza"])
            return {
                "objeto_detectado": decision["objeto_detectado"],
                "categoria": decision["categoria"],
                "accion": decision["accion"],
                "confianza": round(principal["confianza"], 4),
                "instrucciones": decision["instrucciones"],
                "otras_posibilidades": predicciones[1:],
                "label_modelo": principal["label"],
                "modelo": "personalizado",
            }

        predicciones = [
            {
                "label": self._labels[idx],
                "confianza": float(prob),
            }
            for prob, idx in zip(top_probs.tolist(), top_indices.tolist())
        ]
        principal = predicciones[0]
        decision = self._mapear_desde_predicciones(predicciones)
        return {
            "objeto_detectado": decision["objeto_detectado"],
            "categoria": decision["categoria"],
            "accion": decision["accion"],
            "confianza": round(decision.get("confianza", principal["confianza"]), 4),
            "instrucciones": decision["instrucciones"],
            "otras_posibilidades": predicciones[1:],
            "label_modelo": principal["label"],
            "modelo": "base_imagenet",
        }

    def _mapear_clase_personalizada(self, label: str, confianza: float) -> Dict:
        label_norm = label.lower().strip()
        mapping = {
            "plastico": ("plastico", "reciclable", "reciclar", "Depositalo limpio en reciclaje de plastico."),
            "papel": ("papel", "reciclable", "reciclar", "Si esta seco y limpio, llevalo al contenedor de papel."),
            "carton": ("carton", "reciclable", "reciclar", "Aplástalo si puedes y reciclalo con papel/carton."),
            "vidrio": ("vidrio", "reciclable", "reciclar", "Llevalo al contenedor de vidrio."),
            "metal": ("metal", "reciclable", "reciclar", "Depositalo en el flujo de reciclaje de metales."),
            "electronico": (
                "electronico",
                "peligroso",
                "disposicion_especial",
                "Es un residuo electronico. Llevado a un punto RAEE.",
            ),
            "organico": ("organico", "organico", "compostar", "Gestiona este residuo como organico o compostaje."),
            "animal": ("animal", "no_reciclable", "no_desechar", "Eso parece un ser vivo, no un residuo."),
            "no_residuo": ("no_residuo", "no_reciclable", "no_desechar", "No parece un residuo reciclable."),
        }
        objeto, categoria, accion, instrucciones = mapping.get(
            label_norm,
            (
                label,
                "indeterminado",
                "revision_manual",
                "La clase detectada no tiene una regla configurada todavia.",
            ),
        )
        return {
            "objeto_detectado": objeto,
            "categoria": categoria,
            "accion": accion,
            "instrucciones": instrucciones,
            "confianza": confianza,
        }

    def _mapear_desde_predicciones(self, predicciones: List[Dict]) -> Dict:
        for prediccion in predicciones:
            decision = self._mapear_clasificacion(
                prediccion["label"],
                prediccion["confianza"],
                permitir_baja_confianza=False,
            )
            if decision is not None and decision["categoria"] != "indeterminado":
                decision["confianza"] = prediccion["confianza"]
                return decision

        principal = predicciones[0]
        return self._mapear_clasificacion(
            principal["label"],
            principal["confianza"],
            permitir_baja_confianza=True,
        ) or {
            "objeto_detectado": principal["label"],
            "categoria": "indeterminado",
            "accion": "revision_manual",
            "instrucciones": "El modelo detecto un objeto, pero no hay una regla de reciclaje clara para esa etiqueta.",
            "confianza": principal["confianza"],
        }

    def _mapear_clasificacion(
        self,
        label: str,
        confianza: float,
        permitir_baja_confianza: bool,
    ) -> Dict | None:
        label_lower = label.lower()

        if permitir_baja_confianza and confianza < 0.20:
            return {
                "objeto_detectado": label,
                "categoria": "indeterminado",
                "accion": "revision_manual",
                "instrucciones": "La confianza fue baja. Toma otra foto con mejor luz y fondo simple antes de decidir.",
                "confianza": confianza,
            }

        if any(palabra in label_lower for palabra in ["phone", "cellular telephone", "mobile phone", "hand-held computer"]):
            return {
                "objeto_detectado": "telefono",
                "categoria": "peligroso",
                "accion": "disposicion_especial",
                "instrucciones": "Llevalo a un punto de recoleccion de residuos electronicos. No va al reciclaje comun.",
                "confianza": confianza,
            }

        if any(palabra in label_lower for palabra in ["computer", "laptop", "notebook", "monitor", "screen", "television"]):
            return {
                "objeto_detectado": "electronico",
                "categoria": "peligroso",
                "accion": "disposicion_especial",
                "instrucciones": "Es un residuo electronico. Entregalo en un punto autorizado de RAEE.",
                "confianza": confianza,
            }

        if any(palabra in label_lower for palabra in ["bottle", "plastic bag", "water bottle", "milk can", "packet"]):
            return {
                "objeto_detectado": "plastico",
                "categoria": "reciclable",
                "accion": "reciclar",
                "instrucciones": "Enjuagalo si hace falta y depositalo en el contenedor de reciclables.",
                "confianza": confianza,
            }

        if any(palabra in label_lower for palabra in ["wine bottle", "beer bottle", "jar", "glass"]):
            return {
                "objeto_detectado": "vidrio",
                "categoria": "reciclable",
                "accion": "reciclar",
                "instrucciones": "Depositalo en el contenedor de vidrio, limpio y sin tapa.",
                "confianza": confianza,
            }

        if any(palabra in label_lower for palabra in ["carton", "packet", "envelope", "book jacket", "comic book"]):
            return {
                "objeto_detectado": "papel o carton",
                "categoria": "reciclable",
                "accion": "reciclar",
                "instrucciones": "Si esta seco y limpio, llevalo al contenedor de papel y carton.",
                "confianza": confianza,
            }

        if any(
            palabra in label_lower
            for palabra in ["alligator", "crocodile", "caiman", "lizard", "snake", "dog", "cat", "bird", "frog", "turtle"]
        ):
            return {
                "objeto_detectado": label,
                "categoria": "no_reciclable",
                "accion": "no_desechar",
                "instrucciones": "Eso parece un animal o ser vivo. No corresponde a una clasificacion de residuos.",
                "confianza": confianza,
            }

        if any(palabra in label_lower for palabra in ["banana", "orange", "lemon", "pineapple", "cabbage", "broccoli", "mushroom"]):
            return {
                "objeto_detectado": "organico",
                "categoria": "organico",
                "accion": "compostar",
                "instrucciones": "Si es un residuo organico real, puedes compostarlo o gestionarlo como organico.",
                "confianza": confianza,
            }

        if permitir_baja_confianza:
            return {
                "objeto_detectado": label,
                "categoria": "indeterminado",
                "accion": "revision_manual",
                "instrucciones": "El modelo detecto un objeto, pero no hay una regla de reciclaje clara para esa etiqueta.",
                "confianza": confianza,
            }
        return None
