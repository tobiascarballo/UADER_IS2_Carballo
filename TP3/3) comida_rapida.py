# comida rapida con patron factory.py como guia

from abc import ABC, abstractmethod

#clase abstracta
class Entrega(ABC):
    @abstractmethod
    def entregar(self):
        pass

#implementaciones
class EntregaMostrador(Entrega):
    def entregar(self):
        return "Hamburguesa entregada en mostrador."

class EntregaRetiroCliente(Entrega):
    def entregar(self):
        return "Hamburguesa retirada por el cliente."

class EntregaDelivery(Entrega):
    def entregar(self):
        return "Hamburguesa enviada por delivery."


#factory que decide que entrega crear
class EntregaFactory:
    @staticmethod
    def crear_entrega(tipo):
        if tipo == "mostrador":
            return EntregaMostrador()
        elif tipo == "retiro":
            return EntregaRetiroCliente()
        elif tipo == "delivery":
            return EntregaDelivery()
        else:
            raise ValueError("Tipo de entrega no válido")


#clase hamburguesa que utiliza la estrategia de entrega
class Hamburguesa:
    def __init__(self, tipo_entrega):
        self.entrega = EntregaFactory.crear_entrega(tipo_entrega)

    def servir(self):
        return self.entrega.entregar()


#ejemplo
if __name__ == "__main__":
    print("Tipos de entrega disponibles: mostrador, retiro, delivery")
    tipo = input("Ingrese el tipo de entrega: ").lower()

    try:
        h = Hamburguesa(tipo)
        print(h.servir())
    except ValueError as e:
        print("Error:", e)