# factorial con patron singleton.py como guia

class Factorial:
    _instance = None  #atributo estático para guardar la única instancia

    def __new__(cls):
        if cls._instance is None:
            print("Creando instancia de Factorial")
            cls._instance = super(Factorial, cls).__new__(cls)
        return cls._instance

    def calcular(self, n):
        if n < 0:
            raise ValueError("El número debe ser positivo")
        resultado = 1
        for i in range(2, n + 1):
            resultado *= i
        return resultado

#interaccion con usuario para que ingrese un numero
if __name__ == "__main__":
    try:
        numero = int(input("Ingrese un número entero para calcular su factorial: "))
        instancia_factorial = Factorial()
        resultado = instancia_factorial.calcular(numero)
        print(f"El factorial de {numero} es: {resultado}")
    except ValueError as e: #se usa el try/except para corroborar que si el usuario ingreso un caracter invalido, el programa no
        print("Error:", e)