# Dataset de residuos

Pon aqui las imagenes para entrenar el modelo.

## Estructura

```text
dataset/
  train/
    animal/
    carton/
    electronico/
    metal/
    no_residuo/
    organico/
    papel/
    plastico/
    vidrio/
  val/
    animal/
    carton/
    electronico/
    metal/
    no_residuo/
    organico/
    papel/
    plastico/
    vidrio/
```

## Recomendaciones

- Usa fotos reales tomadas con celular cuando puedas.
- Mezcla fondos, angulos y tipos de luz.
- Evita imagenes demasiado parecidas entre si.
- Mueve alrededor de 80% a `train/` y 20% a `val/`.

## Ejemplos por clase

- `plastico`: botellas, envases, tapas, bolsas.
- `papel`: hojas, periodico, cuadernos.
- `carton`: cajas, empaques de carton.
- `vidrio`: frascos, botellas de vidrio.
- `metal`: latas, tapas metalicas, objetos de aluminio.
- `electronico`: telefonos, cargadores, teclados, audifonos.
- `organico`: cascaras, restos de comida, frutas, verduras.
- `animal`: perro, gato, caiman, aves, reptiles.
- `no_residuo`: manos, muebles, ropa, paisaje, personas.
