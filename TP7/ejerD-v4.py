# Copyright UADER-FCyT-IS2©2024 todos los derechos reservados
"""
Versión 1.1 - Refactorización con Branching by Abstraction
Este módulo permite acceder a valores dentro de un archivo JSON.
Puede ejecutarse desde línea de comandos, y aplica el patrón Singleton.
"""

import json
import argparse
import sys
from abc import ABC, abstractmethod


class GetJasonInterface(ABC):
    """Abstracción para la lectura de JSON."""
    @abstractmethod
    def get_value(self, archivo, clave):
        pass


class GetJasonRefactor(GetJasonInterface):
    """Implementación refactorizada del lector JSON usando Singleton."""

    _instance = None
    version = "1.1"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GetJasonRefactor, cls).__new__(cls)
        return cls._instance

    def get_value(self, archivo, clave='token1'):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)

            if clave not in datos:
                print(f"Error: la clave '{clave}' no existe en el archivo.")
                return

            print(datos[clave])

        except FileNotFoundError:
            print(f"Error: el archivo '{archivo}' no se encontró.")
        except json.JSONDecodeError:
            print(f"Error: el archivo '{archivo}' no es un JSON válido.")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description='Lector de valores en archivo JSON.')
    parser.add_argument('archivo_json', type=str, help='Nombre del archivo JSON')
    parser.add_argument('clave', type=str, nargs='?', default='token1', help='Clave a buscar en el archivo')
    parser.add_argument('-v', '--version', action='store_true', help='Muestra la versión del programa')

    args = parser.parse_args()

    if args.version:
        print("getJason versión 1.1")
        sys.exit(0)

    # Acá es donde usamos la abstracción
    lector: GetJasonInterface = GetJasonRefactor()
    lector.get_value(args.archivo_json, args.clave)


if __name__ == '__main__':
    main()
