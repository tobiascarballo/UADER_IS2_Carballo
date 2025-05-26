# getJason.py - versión con patrón Singleton
# Copyright UADER-FCyT-IS2©2024 todos los derechos reservados

import json
import sys


class JasonReader:
    """Clase para leer un archivo JSON y obtener el valor de una clave."""
    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(JasonReader, cls).__new__(cls)
        return cls._instance

    def __init__(self, json_file, json_key='token1'):
        self.json_file = json_file
        self.json_key = json_key
        self.data = None
        self.load_json()

    def load_json(self):
        """Carga el archivo JSON y lo transforma en un diccionario."""
        try:
            with open(self.json_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"Error: El archivo '{self.json_file}' no fue encontrado.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: El archivo no contiene un JSON válido.")
            sys.exit(1)

    def get_value(self):
        """Obtiene el valor asociado a la clave deseada."""
        try:
            return self.data[self.json_key]
        except KeyError:
            print(f"Error: La clave '{self.json_key}' no existe en el archivo.")
            sys.exit(1)

# bloque principal de ejecución

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python getJason.py <archivo_json> [clave]")
        sys.exit(1)

    json_file = sys.argv[1]
    json_key = sys.argv[2] if len(sys.argv) > 2 else 'token1'

    reader = JasonReader(json_file, json_key)
    print(reader.get_value())
