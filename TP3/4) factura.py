# construccion de aviones con patron factory.py como guia

from abc import ABC, abstractmethod

#clase abstracta
class Factura(ABC):
    def __init__(self, importe):
        self.importe = importe

    @abstractmethod
    def mostrar(self):
        pass


#subclases
class FacturaResponsable(Factura):
    def mostrar(self):
        print(f"Factura A - IVA Responsable - Total: ${self.importe:.2f}")

class FacturaNoInscripto(Factura):
    def mostrar(self):
        print(f"Factura C - IVA No Inscripto - Total: ${self.importe:.2f}")

class FacturaExento(Factura):
    def mostrar(self):
        print(f"Factura E - IVA Exento - Total: ${self.importe:.2f}")


#factory
class FacturaFactory:
    @staticmethod
    def crear_factura(condicion, importe):
        condicion = condicion.lower()
        if condicion == "responsable":
            return FacturaResponsable(importe)
        elif condicion == "no inscripto":
            return FacturaNoInscripto(importe)
        elif condicion == "exento":
            return FacturaExento(importe)
        else:
            raise ValueError("Condición impositiva no válida")


#ejemplo
if __name__ == "__main__":
    print("Condiciones posibles: Responsable, No Inscripto, Exento")
    condicion = input("Ingrese la condición impositiva del cliente: ")
    try:
        importe = float(input("Ingrese el importe total de la factura: $"))
        factura = FacturaFactory.crear_factura(condicion, importe)
        factura.mostrar()
    except ValueError as e:
        print("Error:", e)
