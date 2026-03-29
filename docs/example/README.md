# unumbio-pdf-processing-test



import json


# Texto JSON (cadena de texto plana)
texto_json = '{"nombre": "NOVA BRAND", "clase": 25}'

# text plano
print(texto_json)
print(type(texto_json))  # <class 'str'>

# convert to diccionario
data = json.loads(texto_json)
print(data)
print(type(data))  # <class 'dict'>



# Coordenadas en PDF — ¿Para qué sirven?

Imagínate que el PDF es una hoja de papel física y que alguien midió con regla la posición exacta de cada palabra.

---

## El PDF es un plano de coordenadas

```
(0,0) ────────────────────────────► X (horizontal)
  │
  │      [texto aquí x0=50, x1=200]
  │
  │      [otro texto x0=50, x1=200]
  │
  ▼
  Y (vertical, crece hacia abajo)
```

Cada bloque de texto tiene su "dirección" en la página:

| Campo    | Qué mide                  | Analogía                        |
|----------|---------------------------|---------------------------------|
| `x0`     | Borde izquierdo del texto | Desde dónde empieza la palabra  |
| `x1`     | Borde derecho del texto   | Hasta dónde llega la palabra    |
| `top`    | Borde superior            | A qué altura está               |
| `bottom` | Borde inferior            | Hasta qué altura llega          |

---

## Visualmente con un ejemplo

```json
{
    "text": "111",
    "x0": 50,
    "x1": 80,
    "top": 150,
    "bottom": 170
}
```

```
x=0                x=50   x=80
│                    │      │
│                  [111]    │   ← top=150, bottom=170
│                           │
```

---

## ¿Para qué sirve esto en el test?

El PDF tiene **dos columnas**, y PDFPlumber extrae todo el texto mezclado.
Sin coordenadas no sabrías si `"NOVA BRAND"` pertenece a la columna izquierda o derecha:

```
COLUMNA IZQUIERDA    │    COLUMNA DERECHA
─────────────────────│────────────────────
111                  │    111
NOVA BRAND           │    TECHVISION
Clase 25             │    Clase 9
x0=50, x1=280        │    x0=320, x1=550
```

La lógica del test es simplemente:

```python
COLUMNA_DIVISORIA = 300  # punto medio de la página

if texto["x0"] < 300:
    # pertenece a columna IZQUIERDA
else:
    # pertenece a columna DERECHA
```

---

## Ordenar verticalmente

Para saber qué texto va antes y cuál después dentro de una columna,
se usa `top` — el texto con menor `top` aparece más arriba en la página:

```python
# Ordenar por posición vertical
textos_ordenados = sorted(textos, key=lambda t: t["top"])
```

Así sabes que el texto con `top=150` va antes que el de `top=200`.

---

## Resumen — Las coordenadas sirven para 3 cosas

| # | Uso | Campo utilizado |
|---|-----|-----------------|
| 1 | Separar columnas izquierda / derecha | `x0` |
| 2 | Ordenar texto verticalmente | `top` |
| 3 | Agrupar elementos de un mismo registro | `top` (textos cercanos) |

---

## Flujo general del script

```
Leer JSON
    │
    ▼
Por cada página
    │
    ▼
Separar textos por columna (x0 < 300 → izquierda, x0 >= 300 → derecha)
    │
    ▼
Ordenar cada columna por top (de menor a mayor)
    │
    ▼
Identificar registros (comienzan con código INID, ej: "111")
    │
    ▼
Agrupar campos de cada registro
    │
    ▼
Guardar en JSON de salida
``` 