import json


# Create .json
data_simation = {
    "paginas": [
        {
            "page": 1,
            "textboxhorizontal": [
                {
                    "text": "B.1 MARCAS REGISTRADAS",
                    "x0": 50,
                    "x1": 200,
                    "top": 100,
                    "bottom": 120,
                },
                {"text": "111", "x0": 50, "x1": 80, "top": 150, "bottom": 170},
                {"text": "NOVA BRAND", "x0": 90, "x1": 300, "top": 150, "bottom": 170},
            ],
        }
    ]
}


# savegin disc    encoding="utf-8"
with open("prueba.json", "w", encoding="utf-8") as f:
    json.dump(data_simation, f, ensure_ascii=False, indent=4)
# qque representa la w ?
# porque encoding ?
# porque la f cuando se convierten   ?  and ensure_ascii=False, indent=4 ? ?

print("Archivo creado exitosamente!")

# Leer desde disco
with open("prueba.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(type(data))  # <class 'dict'>
print(data["paginas"])  # lista de páginas


"""

"w"write — abre el archivo para escribir. Si no existe lo crea, si existe lo sobreescribe
"r"read — abre el archivo solo para leer
"a"append — agrega al final sin borrar lo que habíaas


-- 

¿Por qué encoding="utf-8"?
Porque los archivos de texto necesitan saber cómo interpretar los caracteres. 
Sin esto, las tildes y la ñ pueden corromperse o generar error:
"NOVA BRAND"  →  "NOVA BR��ND"   # ❌

--

¿Por qué ensure_ascii=False e indent=4?
ensure_ascii=False → permite guardar tildes y ñ directamente:
- ensure_ascii=True  (default, malo para español)
{"nombre": "Registraci\u00f3n"}

-  ensure_ascii=False  (lo que quieres)
{"nombre": "Registración"}

-- 
indent=4 → hace el JSON legible para humanos:
-> Sin indent (todo en una línea, ilegible)
{"paginas": [{"page": 1, "texto": "hola"}]}

-> Con indent=4 (ordenado y legible)
{
    "paginas": [
        {
            "page": 1,
            "texto": "hola"
        }
    ]
}


"""
