# construccion de aviones con patron prototype.py como guia

class Note:
    def __init__(self, fraction):
        self.fraction = fraction

    def get(self):
        return self.fraction

    def clone(self):
        return Note(self.fraction)


#prueba de clonacion de cadena
if __name__ == "__main__":
    original = Note(10)
    print(f"Original: {original.get()}")

    copia1 = original.clone()
    print(f"Copia1: {copia1.get()}")

    copia2 = copia1.clone()
    print(f"Copia2 (de la copia1): {copia2.get()}")

    # Verificamos que son objetos distintos
    print(f"¿Original y Copia1 son el mismo objeto?: {original is copia1}")
    print(f"¿Copia1 y Copia2 son el mismo objeto?: {copia1 is copia2}")
