from abc import ABC, abstractmethod

# Sujeto (Subject)
class EmisorID:
    def __init__(self):
        self.observadores = []

    def agregar_observador(self, observador):
        self.observadores.append(observador)

    def emitir_id(self, id_emitido):
        print(f"\nEmisor: Emite ID '{id_emitido}'")
        for observador in self.observadores:
            observador.actualizar(id_emitido)

# Interfaz Observer
class ObservadorID(ABC):
    def __init__(self, id_propio):
        self.id_propio = id_propio

    @abstractmethod
    def actualizar(self, id_emitido):
        pass

# Observadores concretos
class ClaseA(ObservadorID):
    def actualizar(self, id_emitido):
        if id_emitido == self.id_propio:
            print(f"ClaseA: ID coincidente '{id_emitido}' detectado!")

class ClaseB(ObservadorID):
    def actualizar(self, id_emitido):
        if id_emitido == self.id_propio:
            print(f"ClaseB: ID coincidente '{id_emitido}' detectado!")

class ClaseC(ObservadorID):
    def actualizar(self, id_emitido):
        if id_emitido == self.id_propio:
            print(f"ClaseC: ID coincidente '{id_emitido}' detectado!")

class ClaseD(ObservadorID):
    def actualizar(self, id_emitido):
        if id_emitido == self.id_propio:
            print(f"ClaseD: ID coincidente '{id_emitido}' detectado!")

# Configuración del patrón Observer
emisor = EmisorID()

# Crear 4 observadores con diferentes IDs
obs1 = ClaseA("AB12")
obs2 = ClaseB("CD34")
obs3 = ClaseC("EF56")
obs4 = ClaseD("GH78")

# Subscribir observadores
emisor.agregar_observador(obs1)
emisor.agregar_observador(obs2)
emisor.agregar_observador(obs3)
emisor.agregar_observador(obs4)

# Emitir 8 IDs (4 deben coincidir)
ids_a_emitir = ["AB12", "XXXX", "CD34", "YYYY", "EF56", "ZZZZ", "GH78", "AAAA"]
for id_emitido in ids_a_emitir:
    emisor.emitir_id(id_emitido)
