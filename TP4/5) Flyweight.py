class CaracterFlyweight:
    def __init__(self, fuente, tamaño, color):
        self.fuente = fuente
        self.tamaño = tamaño
        self.color = color

    def mostrar(self, letra, posicion):
        print(f"Letra '{letra}' en pos {posicion} con fuente={self.fuente}, tamaño={self.tamaño}, color={self.color}")

class FlyweightFactory:
    def __init__(self):
        self._flyweights = {}

    def obtener_flyweight(self, fuente, tamaño, color):
        clave = (fuente, tamaño, color)
        if clave not in self._flyweights:
            self._flyweights[clave] = CaracterFlyweight(fuente, tamaño, color)
        return self._flyweights[clave]

# Cliente
class Caracter:
    def __init__(self, letra, posicion, flyweight):
        self.letra = letra
        self.posicion = posicion
        self.flyweight = flyweight

    def mostrar(self):
        self.flyweight.mostrar(self.letra, self.posicion)


if __name__ == "__main__":
    factory = FlyweightFactory()

    estilo1 = factory.obtener_flyweight("Arial", 12, "Negro")
    estilo2 = factory.obtener_flyweight("Arial", 12, "Negro")
    estilo3 = factory.obtener_flyweight("Courier", 10, "Rojo")

    letra1 = Caracter("H", (0, 0), estilo1)
    letra2 = Caracter("o", (0, 1), estilo2)
    letra3 = Caracter("!", (0, 2), estilo3)

    letra1.mostrar()
    letra2.mostrar()
    letra3.mostrar()
