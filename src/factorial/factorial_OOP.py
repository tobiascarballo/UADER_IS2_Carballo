#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial_OOP.py                                                         *
#* Calcula el factorial de un número o de un rango de números utilizando   *
#* programación orientada a objetos (OOP).                                 *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*

import sys

# Definimos la clase Factorial
class Factorial:
    def __init__(self, num=None):
        # Constructor que inicializa el número (num) o el rango
        self.num = num

    # Método para calcular el factorial de un número
    def factorial(self, num): 
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

    # Método para calcular el factorial de un rango de números
    def run(self, min_num, max_num):
        for i in range(min_num, max_num + 1):
            print(f"El factorial de {i} es: {self.factorial(i)}")

# Lógica para recibir un número o un rango de números desde la línea de comandos
if len(sys.argv) == 1:
    num = int(input("Por favor, ingrese un número para calcular su factorial: "))
    factorial = Factorial(num)
    print("Factorial ", num, "! es ", factorial.factorial(num))
elif '-' in sys.argv[1]:
    rango = sys.argv[1]
    if rango.startswith('-'):  # Caso sin límite inferior
        fin = int(rango[1:])
        factorial = Factorial()
        factorial.run(1, fin)
        sys.exit()  # Salimos después de calcular el rango
    elif rango.endswith('-'):  # Caso sin límite superior
        inicio = int(rango[:-1])
        factorial = Factorial()
        factorial.run(inicio, 60)
        sys.exit()  # Salimos después de calcular el rango
    else:
        inicio, fin = map(int, rango.split('-'))
        factorial = Factorial()
        factorial.run(inicio, fin)
        sys.exit()  # Salimos después de calcular el rango
else:
    num = int(sys.argv[1])
    factorial = Factorial(num)
    print("Factorial ", num, "! es ", factorial.factorial(num))
