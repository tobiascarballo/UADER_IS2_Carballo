# Copyright UADER-FCyT-IS2©2024 - Todos los derechos reservados

"""
getJason.py - versión 1.2
Script para obtener el valor de una clave desde un archivo JSON.
Implementa patrón Singleton, validación de argumentos, control de errores,
y robustecimiento de la ejecución desde línea de comandos.
"""

import json
import sys
import os

class JsonReaderSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JsonReaderSingleton, cls).__new__(cls)
        return cls._instance

    def get_value(self, json_file, key='token1'):
        if not os.path.exists(json_file):
            return f"Error: el archivo '{json_file}' no existe."

        try:
            with open(json_file, 'r') as f:
                data = json.load(f)

            if key in data:
                return data[key]
            else:
                return f"Error: la clave '{key}' no existe en el archivo."
        except json.JSONDecodeError:
            return "Error: el archivo no contiene un JSON válido."
        except Exception as e:
            return f"Error inesperado: {e}"

def main():
    # Mostrar versión si se pasa el argumento -v
    if len(sys.argv) == 2 and sys.argv[1] == "-v":
        print("Versión 1.2")
        return

    # Validar cantidad de argumentos
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Uso correcto:")
        print("  python getJason.py <archivo_json> [clave]")
        print("  python getJason.py -v  # Para ver la versión")
        return

    json_file = sys.argv[1]

    # Validación: archivo debe tener extensión .json
    if not json_file.endswith('.json'):
        print("Error: el archivo debe tener extensión .json")
        return

    # Clave opcional, por defecto 'token1'
    key = sys.argv[2] if len(sys.argv) == 3 else 'token1'

    # Ejecutar funcionalidad
    reader = JsonReaderSingleton()
    result = reader.get_value(json_file, key)
    print(result)

if __name__ == "__main__":
    main()
