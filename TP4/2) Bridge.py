#Implementación del tren laminador (Implementor)
class TrenLaminador:
    def producir(self, largo):
        raise NotImplementedError("Método abstracto")

# Tren laminador de 5 metros (ConcreteImplementor A)
class TrenLaminador5m(TrenLaminador):
    def producir(self, largo):
        print(f"Produciendo una lámina de {largo} metros con tren de 5 metros.")

# Tren laminador de 10 metros (ConcreteImplementor B)
class TrenLaminador10m(TrenLaminador):
    def producir(self, largo):
        print(f"Produciendo una lámina de {largo} metros con tren de 10 metros.")

# Abstracción: lámina de acero (Abstraction)
class LaminaAcero:
    def __init__(self, espesor, ancho, largo, tren_laminador: TrenLaminador):
        self.espesor = espesor
        self.ancho = ancho
        self.largo = largo
        self.tren = tren_laminador

    def producir(self):
        print(f"Lámina de {self.espesor}'' de espesor, {self.ancho}m de ancho.")
        self.tren.producir(self.largo)

#Prueba de ejecución

if __name__ == "__main__":
    tren5 = TrenLaminador5m()
    tren10 = TrenLaminador10m()

    # Crear láminas con distintos trenes
    lamina1 = LaminaAcero(0.5, 1.5, 5, tren5)
    lamina2 = LaminaAcero(0.5, 1.5, 10, tren10)

    lamina1.producir()
    lamina2.producir()