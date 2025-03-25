#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* collatz.py                                                              *
#* Calcula la secuencia de Collatz (conjetura 2n + 1) para los números      *
#* entre 1 y 10,000 y grafica el número de iteraciones necesarias para     *
#* llegar a una secuencia repetitiva.                                      *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*

import matplotlib.pyplot as plt

# Función para calcular el número de iteraciones de la secuencia de Collatz
def collatz_iterations(n):
    count = 0
    while n != 1:
        if n % 2 == 0:  # Si el número es par
            n = n // 2
        else:  # Si el número es impar
            n = 3 * n + 1
        count += 1  # Incrementamos el contador de iteraciones
    return count

# Lista para almacenar los números de inicio y sus iteraciones
numbers = []
iterations = []

# Calculamos la secuencia de Collatz para los números entre 1 y 10,000
for i in range(1, 10001):
    numbers.append(i)
    iterations.append(collatz_iterations(i))

# Realizamos el gráfico
plt.figure(figsize=(10, 6))
plt.scatter(iterations, numbers, s=1, color='blue')
plt.title('Número de iteraciones de la secuencia de Collatz (1-10000)', fontsize=14)
plt.xlabel('Número de iteraciones', fontsize=12)
plt.ylabel('Número de inicio de la secuencia', fontsize=12)
plt.grid(True)
plt.show()
