# Copyright UADER-FCyT-IS2©2024 - Todos los derechos reservados

"""
getJason.py - versión 1.1
Script para obtener el valor de una clave desde un archivo JSON.
Implementa patrón Singleton, validación de argumentos, y control de errores.
"""

import json
import sys
import os

class JsonReaderSingleton:
    """
    Clase Singleton para leer archivos JSON y obtener claves específicas.
    """
    _instance = None

    def __new__(cls):
        # Garantiza que solo se cree una instancia del objeto
        if cls._instance is None:
            cls._instance = super(JsonReaderSingleton, cls).__new__(cls)
        return cls._instance

    def get_value(self, json_file, key='token1'):
        """
        Intenta abrir el archivo JSON y devolver el valor asociado a la clave dada.
        Devuelve un mensaje de error controlado si ocurre una excepción.
        """
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            if key in data:
                return data[key]
            else:
                return f"Error: la clave '{key}' no existe en el archivo."
        except FileNotFoundError:
            return f"Error: el archivo '{json_file}' no fue encontrado."
        except json.JSONDecodeError:
            return "Error: el contenido del archivo no es un JSON válido."
        except Exception as e:
            return f"Error inesperado: {e}"

def main():
    # Si se invoca con -v, se muestra la versión del programa
    if len(sys.argv) == 2 and sys.argv[1] == "-v":
        print("Versión 1.1")
        return

    # Chequeo de argumentos (mínimo 1: archivo JSON)
    if len(sys.argv) < 2:
        print("Uso: python getJason.py <archivo_json> [clave]")
        return

    json_file = sys.argv[1]
    key = sys.argv[2] if len(sys.argv) > 2 else 'token1'

    # Obtención del Singleton y llamada al método
    reader = JsonReaderSingleton()
    result = reader.get_value(json_file, key)
    print(result)

if __name__ == "__main__":
    main()
