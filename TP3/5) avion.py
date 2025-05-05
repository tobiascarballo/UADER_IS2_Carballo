# construccion de aviones con patron builder.py como guia

class Avion:
    def __init__(self):
        self.body = None
        self.turbinas = []
        self.alas = []
        self.tren_aterrizaje = None

    def mostrar_componentes(self):
        print("   Avión construido con:")
        print(f"- Cuerpo: {self.body}")
        print(f"- {len(self.turbinas)} turbinas")
        print(f"- {len(self.alas)} alas")
        print(f"- Tren de aterrizaje: {self.tren_aterrizaje}")


class AvionBuilder:
    def __init__(self):
        self.avion = Avion()

    def construir_body(self):
        self.avion.body = "Fuselaje estándar"

    def construir_turbinas(self):
        self.avion.turbinas.append("Turbina izquierda")
        self.avion.turbinas.append("Turbina derecha")

    def construir_alas(self):
        self.avion.alas.append("Ala izquierda")
        self.avion.alas.append("Ala derecha")

    def construir_tren_aterrizaje(self):
        self.avion.tren_aterrizaje = "Tren retráctil"

    def obtener_avion(self):
        return self.avion


#parte del cliente
if __name__ == "__main__":
    builder = AvionBuilder()
    builder.construir_body()
    builder.construir_turbinas()
    builder.construir_alas()
    builder.construir_tren_aterrizaje()

    avion = builder.obtener_avion()
    avion.mostrar_componentes()
