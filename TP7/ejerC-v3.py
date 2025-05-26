#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
getJason_v3_singleton.py
Versión 3 - Agregado de robustez en ejecución desde línea de comandos

Copyright UADER-FCyT-IS2 ©2024 - Todos los derechos reservados
"""

import json
import argparse
import os
import sys


class JasonReaderSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JasonReaderSingleton, cls).__new__(cls)
        return cls._instance

    def read_key(self, filepath, key="token1"):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Error: el archivo '{filepath}' no fue encontrado.")
            return None
        except json.JSONDecodeError:
            print(f"Error: el archivo '{filepath}' no tiene un formato JSON válido.")
            return None

        if key not in data:
            print(f"Error: la clave '{key}' no existe en el archivo.")
            return None

        return data[key]


def main():
    parser = argparse.ArgumentParser(description="Lee una clave de un archivo JSON.")
    parser.add_argument("archivo_json", help="Ruta del archivo JSON")
    parser.add_argument("clave", nargs='?', default="token1", help="Clave a buscar en el JSON (por defecto 'token1')")

    args = parser.parse_args()

    lector = JasonReaderSingleton()
    resultado = lector.read_key(args.archivo_json, args.clave)

    if resultado is not None:
        print(f"Valor encontrado: {resultado}")
    else:
        sys.exit(1)  # Finaliza con error controlado si hubo problemas


if __name__ == "__main__":
    main()
