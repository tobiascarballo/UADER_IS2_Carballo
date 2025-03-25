#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys

# Función que calcula el factorial de un número
def factorial(num): 
    # Si el número es negativo, el factorial no existe
    if num < 0: 
        print("Factorial de un número negativo no existe")
        return 0
    # Si el número es cero, el factorial es 1
    elif num == 0: 
        return 1
    else: 
        # Inicializamos la variable fact con 1
        fact = 1
        # Calculamos el factorial multiplicando el número por los enteros anteriores
        while(num > 1): 
            fact *= num 
            num -= 1  # Reducimos el número en 1
        return fact  # Devolvemos el resultado final del factorial

# Verificamos si se proporcionó un argumento en la línea de comandos
if len(sys.argv) == 1:
    # Si no se proporciona un argumento, pedimos al usuario que ingrese un número
    num = int(input("Por favor, ingrese un número para calcular su factorial: "))
elif '-' in sys.argv[1]:
    # Si el argumento contiene un guion, asumimos que es un rango de números
    rango = sys.argv[1]
    # Si el rango comienza con un guion (caso sin límite inferior)
    if rango.startswith('-'):  
        fin = int(rango[1:])  # Extraemos el valor final del rango
        # Calculamos el factorial para los números entre 1 y el valor final
        for i in range(1, fin + 1):
            print(f"El factorial de {i} es: {factorial(i)}")
        sys.exit()  # Salimos después de calcular el rango
    # Si el rango termina con un guion (caso sin límite superior)
    elif rango.endswith('-'):  
        inicio = int(rango[:-1])  # Extraemos el valor inicial del rango
        # Calculamos el factorial para los números entre el valor inicial y 60
        for i in range(inicio, 61):
            print(f"El factorial de {i} es: {factorial(i)}")
        sys.exit()  # Salimos después de calcular el rango
    else:
        # Si el rango tiene un valor de inicio y fin (ej. 4-8)
        inicio, fin = map(int, rango.split('-'))
        # Calculamos el factorial para los números entre el valor de inicio y fin
        for i in range(inicio, fin + 1):
            print(f"El factorial de {i} es: {factorial(i)}")
        sys.exit()  # Salimos después de calcular el rango
else:
    # Si se proporciona un solo número, calculamos su factorial
    num = int(sys.argv[1])

# Imprimimos el resultado del factorial para el número proporcionado
print("Factorial ", num, "! es ", factorial(num))