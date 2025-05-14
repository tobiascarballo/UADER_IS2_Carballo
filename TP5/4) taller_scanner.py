import os

class State:
    def scan(self):
        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0
        print("Sintonizando... Estación {} {}".format(self.stations[self.pos], self.name))

class AmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ["1250", "1380", "1510"]
        self.pos = 0
        self.name = "AM"

    def toggle_amfm(self):
        print("Cambiando a FM")
        self.radio.state = self.radio.fmstate

class FmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ["81.3", "89.1", "103.9"]
        self.pos = 0
        self.name = "FM"

    def toggle_amfm(self):
        print("Cambiando a AM")
        self.radio.state = self.radio.amstate

class MemoryState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = [("M1", "1250 AM"), ("M2", "89.1 FM"), ("M3", "1510 AM"), ("M4", "103.9 FM")]
        self.pos = 0
        self.name = "Memoria"

    def toggle_amfm(self):
        print("Cambiando a FM")
        self.radio.state = self.radio.fmstate

    def scan(self):
        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0
        etiqueta, frecuencia = self.stations[self.pos]
        print(f"Sintonizando... {etiqueta}: {frecuencia}")

class Radio:
    def __init__(self):
        self.fmstate = FmState(self)
        self.amstate = AmState(self)
        self.memstate = MemoryState(self)
        self.states = [self.fmstate, self.amstate, self.memstate]
        self.state_index = 0
        self.state = self.states[self.state_index]

    def toggle_amfm(self):
        self.state_index = (self.state_index + 1) % len(self.states)
        self.state = self.states[self.state_index]
        print(f"Cambiando a {self.state.name}")

    def scan(self):
        self.state.scan()

if __name__ == "__main__":
    os.system("clear")
    print("Crea un objeto radio y almacena las siguientes acciones")
    radio = Radio()
    actions = [radio.scan] * 4 + [radio.toggle_amfm] + [radio.scan] * 4 + [radio.toggle_amfm] + [radio.scan] * 4
    print("Recorre las acciones ejecutando la acción, el objeto cambia la interfaz según el estado")
    for action in actions:
        action()
