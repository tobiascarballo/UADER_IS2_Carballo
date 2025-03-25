#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys

# Función para calcular el factorial de un número
def factorial(num): 
    if num < 0: 
        print("Factorial de un número negativo no existe")
        return 0
    elif num == 0: 
        return 1
    else: 
        fact = 1
        while(num > 1): 
            fact *= num 
            num -= 1
        return fact 

# Lógica para recibir un número o un rango de números
if len(sys.argv) == 1:
    num = int(input("Por favor, ingrese un número para calcular su factorial: "))
elif '-' in sys.argv[1]:
    rango = sys.argv[1]
    if rango.startswith('-'):  # Caso sin límite inferior
        fin = int(rango[1:])
        for i in range(1, fin + 1):
            print(f"El factorial de {i} es: {factorial(i)}")
        sys.exit()
    elif rango.endswith('-'):  # Caso sin límite superior
        inicio = int(rango[:-1])
        for i in range(inicio, 61):
            print(f"El factorial de {i} es: {factorial(i)}")
        sys.exit() 
    else:
        inicio, fin = map(int, rango.split('-'))
        for i in range(inicio, fin + 1):
            print(f"El factorial de {i} es: {factorial(i)}")
        sys.exit()
else:
    num = int(sys.argv[1])

print("Factorial ", num, "! es ", factorial(num))