import json
import sys

# Verificar que al menos se haya pasado el archivo JSON como argumento
if len(sys.argv) < 2:
    print("Uso: python getJason.py <archivo_json> [clave]")
    sys.exit(1)

# El primer argumento es el nombre del archivo JSON
jsonfile = sys.argv[1]

# El segundo argumento (opcional) es la clave a buscar; por defecto es 'token1'
jsonkey = sys.argv[2] if len(sys.argv) > 2 else 'token1'

# Abrir y leer el archivo JSON
with open(jsonfile, 'r') as myfile:
    data = myfile.read()

# Convertir el contenido del archivo a un diccionario
obj = json.loads(data)

# Mostrar por pantalla el valor asociado a la clave solicitada
print(obj[jsonkey])
