# Copyright UADER-FCyT-IS2©2024 - Todos los derechos reservados

"""
getJason.py - versión 1.1
Script para obtener el valor de una clave desde un archivo JSON.
Implementa patrón Singleton, validación de argumentos, control de errores,
y soporte para mostrar la versión del programa con el argumento -v.
"""

import json
import sys
import os


class JsonReaderSingleton:
    """Clase Singleton para lectura de archivos JSON."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_value(self, json_file, key='token1'):
        """Devuelve el valor asociado a una clave desde un archivo JSON."""
        if not os.path.exists(json_file):
            return f"Error: el archivo '{json_file}' no existe."

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if key in data:
                return data[key]

            return f"Error: la clave '{key}' no existe en el archivo."

        except json.JSONDecodeError:
            return "Error: el archivo no contiene un JSON válido."
        except Exception as e:
            return f"Error inesperado: {e}"


def mostrar_uso():
    """Imprime el uso correcto del programa."""
    print("Uso correcto:")
    print("  python getJason.py <archivo_json> [clave]")
    print("  python getJason.py -v  # Para ver la versión")


def main():
    """Función principal del programa."""
    # Soporte para el argumento -v
    if len(sys.argv) == 2 and sys.argv[1] == "-v":
        print("Versión 1.1")
        return

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        mostrar_uso()
        return

    json_file = sys.argv[1]

    if not json_file.endswith('.json'):
        print("Error: el archivo debe tener extensión .json")
        return

    key = sys.argv[2] if len(sys.argv) == 3 else 'token1'

    reader = JsonReaderSingleton()
    resultado = reader.get_value(json_file, key)
    print(resultado)


if __name__ == "__main__":
    main()
