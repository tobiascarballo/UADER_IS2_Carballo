"""
Programa cliente para interactuar con modelos de lenguaje a través de la API de Together AI.

Este script permite:
- Leer consultas del usuario desde consola
- Repetir la última consulta presionando Enter
- Llamar a un modelo de lenguaje (por defecto, Mixtral)
- Imprimir la respuesta recibida con el formato "chatGPT:"
- Manejar errores por bloques separados
"""

import os
import sys  # Para acceder a variables de entorno
from together import Together  # Cliente oficial de la API de Together AI

def obtener_cliente_api():
    """
    Obtiene la clave API desde una variable de entorno y configura el cliente Together.

    Returns:
        Together: Objeto cliente configurado
    """
    api_key = os.environ.get("TOGETHER_API_KEY")  # Leer la variable de entorno
    if not api_key:
        # Mensaje de error si no se encuentra la API key
        print("Error: No se encontró la variable de entorno TOGETHER_API_KEY")
        print("Configúrala con: set TOGETHER_API_KEY=tu_api_key (en Windows CMD)")
        sys.exit(1)

    return Together(api_key=api_key)  # Devolver el cliente configurado

def consultar_modelo(prompt, modelo="mistralai/Mixtral-8x7B-Instruct-v0.1"):
    """
    Envía la consulta al modelo de lenguaje y retorna la respuesta.

    Args:
        prompt (str): Consulta del usuario
        modelo (str): Nombre del modelo a utilizar

    Returns:
        str: Respuesta del modelo o None si hubo error
    """
    try:
        # Llamada a la API con los parámetros definidos
        respuesta = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # Nivel de aleatoriedad
            max_tokens=1024,  # Máxima cantidad de tokens en la respuesta
        )

        # Retornar el contenido de la respuesta
        return respuesta.choices[0].message.content
    except Exception as error:
        # Mostrar mensaje en caso de error
        print(f"Error al comunicarse con la API de Together: {error}")
        return None

def main():
    """
    Función principal que gestiona la interacción completa con el usuario.

    Se divide en tres bloques:
    1. Lectura de entrada del usuario
    2. Procesamiento de la consulta (validaciones y repetición)
    3. Invocación a la API y despliegue de la respuesta
    """
    ultima_consulta = ""  # Guarda la última consulta válida

    while True:
        try:
            # Bloque 1: Lectura de la consulta desde consola
            consulta = input("Ingrese su consulta ('salir' para terminar, Enter = repetir): ")
        except Exception as error:
            # Captura cualquier error de lectura
            print(f"Error al leer la consulta: {error}")
            continue

        try:
            # Bloque 2: Validación de la entrada
            if consulta.lower() == "salir":
                # Finalizar el programa si el usuario desea salir
                print("Programa finalizado.")
                break

            if not consulta.strip():
                # Si se presiona Enter sin texto, repetir la última si existe
                if ultima_consulta == "":
                    print("No hay consulta anterior para repetir.")
                    continue
                consulta = ultima_consulta
                print("(Consulta repetida automáticamente)")
            else:
                # Guardar la nueva consulta como última válida
                ultima_consulta = consulta

            # Mostrar la consulta formateada
            print(f"You: {consulta}")
        except Exception as error:
            # Errores en el procesamiento de la consulta
            print(f"Error al procesar la consulta: {error}")
            continue

        try:
            # Bloque 3: Enviar la consulta al modelo y mostrar respuesta
            respuesta = consultar_modelo(consulta)
            if respuesta:
                print(f"chatGPT: {respuesta}")  # Imprimir respuesta
            else:
                print("No se obtuvo respuesta del modelo.")
        except Exception as error:
            # Capturar errores en la llamada a la API
            print(f"Error al invocar la API: {error}")

# Inicialización del cliente (se hace una sola vez)
client = obtener_cliente_api()

# Punto de entrada del programa
if __name__ == "__main__":
    main()
