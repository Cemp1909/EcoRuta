# Entrenamiento del modelo de residuos

## Estructura esperada del dataset

```text
ia-service/
  dataset/
    train/
      plastico/
      papel/
      carton/
      vidrio/
      metal/
      electronico/
      organico/
      animal/
      no_residuo/
    val/
      plastico/
      papel/
      carton/
      vidrio/
      metal/
      electronico/
      organico/
      animal/
      no_residuo/
```

Cada carpeta debe contener imagenes `.jpg`, `.jpeg` o `.png` de esa clase.

## Recomendaciones

- Empieza con 200 a 500 imagenes por clase.
- Usa fotos con fondos distintos, angulos distintos y luz distinta.
- Pon en `no_residuo` cosas que la app no debe tratar como basura.
- Pon en `animal` ejemplos como perro, gato, caiman, aves o reptiles.

## Comando de entrenamiento

Desde `ia-service/`:

```powershell
.\ecoruta\Scripts\python.exe .\train_residuos.py --data-dir .\dataset --epochs 8 --batch-size 16
```

El modelo entrenado se guarda en:

```text
vision/modelo_residuos.pth
```

## Uso en el backend

No hay que cambiar codigo extra. Cuando exista `vision/modelo_residuos.pth`, el backend lo cargara automaticamente al iniciar.

## Flujo recomendado

1. Crear dataset con `train/` y `val/`.
2. Ejecutar `train_residuos.py`.
3. Reiniciar `app.py`.
4. Probar desde la app Flutter.
