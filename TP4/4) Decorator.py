# Componente base
class Numero:
    def mostrar(self):
        raise NotImplementedError("Método abstracto")

# Implementación concreta del número
class NumeroConcreto(Numero):
    def __init__(self, valor):
        self.valor = valor

    def mostrar(self):
        return self.valor

# Decorador base
class Decorador(Numero):
    def __init__(self, componente: Numero):
        self.componente = componente

    def mostrar(self):
        return self.componente.mostrar()

# Decoradores específicos
class SumarDos(Decorador):
    def mostrar(self):
        return self.componente.mostrar() + 2

class MultiplicarPorDos(Decorador):
    def mostrar(self):
        return self.componente.mostrar() * 2

class DividirPorTres(Decorador):
    def mostrar(self):
        return self.componente.mostrar() / 3


if __name__ == "__main__":
    base = NumeroConcreto(9)
    print("Número original:", base.mostrar())

    decorado1 = SumarDos(base)
    print("Sumar 2:", decorado1.mostrar())

    decorado2 = MultiplicarPorDos(decorado1)
    print("Luego multiplicar por 2:", decorado2.mostrar())

    decorado3 = DividirPorTres(decorado2)
    print("Luego dividir por 3:", decorado3.mostrar())

    # O todo anidado directamente
    resultado = DividirPorTres(MultiplicarPorDos(SumarDos(base)))
    print("Resultado anidado:", resultado.mostrar())