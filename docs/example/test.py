"""
# texto es un diccionario completo, por ejemplo:
texto = {"text": "NOVA BRAND", "x0": 50, "x1": 200, "top": 130, "bottom": 150}

# texto["x0"] → accede al valor de la clave "x0"
print(texto["x0"])  # 50

# COLUMNA_DIVISORIA = 300  (la definimos antes)

# entonces la condición es:
# ¿50 < 300?  → True → va a columna izquierda ✅

# .append(texto) → mete el diccionario COMPLETO en la lista
# no solo el texto, sino todo el diccionario con sus coordenadas
columna_izquierda.append(texto)

# resultado:
# columna_izquierda = [
#     {"text": "NOVA BRAND", "x0": 50, "x1": 200, "top": 130, "bottom": 150}
# ]
```

---

## Visualmente el flujo completo:
```
textboxhorizontal (todos mezclados)
│
│  {"text": "NOVA BRAND", "x0": 50  ...}  → x0=50  < 300 → izquierda ✅
│  {"text": "TECHVISION", "x0": 320 ...}  → x0=320 > 300 → derecha  ✅
│  {"text": "Clase 25",   "x0": 50  ...}  → x0=50  < 300 → izquierda ✅
│  {"text": "Clase 9",    "x0": 320 ...}  → x0=320 > 300 → derecha  ✅
▼
columna_izquierda = [NOVA BRAND, Clase 25]
columna_derecha   = [TECHVISION, Clase 9]

"""

import json

# Simulamos lo que vendría del archivo _001.json
pagina = {
    "page": 1,
    "textboxhorizontal": [
        {"text": "111", "x0": 50, "x1": 80, "top": 100, "bottom": 120},
        {"text": "NOVA BRAND", "x0": 50, "x1": 200, "top": 130, "bottom": 150},
        {"text": "Clase 25", "x0": 50, "x1": 150, "top": 160, "bottom": 180},
        {"text": "111", "x0": 320, "x1": 350, "top": 100, "bottom": 120},
        {"text": "TECHVISION", "x0": 320, "x1": 480, "top": 130, "bottom": 150},
        {"text": "Clase 9", "x0": 320, "x1": 420, "top": 160, "bottom": 180},
    ],
}

print("🚀 ", pagina)

# --- Tu lógica aquí ---
COLUMNA_DIVISORIA = 300

columna_izquierda = []
columna_derecha = []


for texto in pagina["textboxhorizontal"]:
    if texto["x0"] < COLUMNA_DIVISORIA:
        columna_izquierda.append(texto)
    else:
        columna_derecha.append(texto)


# Ordenar cada columna verticalmente
# lambda t: t["top"]  significa:
# "para cada elemento t de la lista, usa t["top"] como criterio de orden"
# es una función anónima de una sola línea
# sorted() es una función nativa de Python que ordena cualquier lista y devuelve una lista nueva:
# lista = [3, 1, 2]
# sorted(lista)  # [1, 2, 3]
columna_izquierda = sorted(columna_izquierda, key=lambda t: t["top"])
columna_derecha = sorted(columna_derecha, key=lambda t: t["top"])

# Ver resultados
print("=== COLUMNA IZQUIERDA ===")
for t in columna_izquierda:
    print(f"  top={t['top']} → {t['text']}")

print("\n=== COLUMNA DERECHA ===")
for t in columna_derecha:
    print(f"  top={t['top']} → {t['text']}")


"""
🚀  {'page': 1, 'textboxhorizontal': [{'text': '111', 'x0': 50, 'x1': 80, 'top': 100, 'bottom': 120}, {'text': 'NOVA BRAND', 'x0': 50, 'x1': 200, 'top': 130, 'bottom': 150}, {'text': 'Clase 25', 'x0': 50, 'x1': 150, 'top': 160, 'bottom': 180}, {'text': '111', 'x0': 320, 'x1': 350, 'top': 100, 'bottom': 120}, {'text': 'TECHVISION', 'x0': 320, 'x1': 480, 'top': 130, 'bottom': 150}, {'text': 'Clase 9', 'x0': 320, 'x1': 420, 'top': 160, 'bottom': 180}]}
=== COLUMNA IZQUIERDA ===
  top=100 → 111
  top=130 → NOVA BRAND
  top=160 → Clase 25

=== COLUMNA DERECHA ===
  top=100 → 111
  top=130 → TECHVISION
  top=160 → Clase 9


"""
