import os
#*--------------------------------------------------------------------
#* Design pattern memento, modificado para múltiples versiones
#*-------------------------------------------------------------------

class Memento:
    def __init__(self, file, content):
        self.file = file
        self.content = content

class FileWriterUtility:
    def __init__(self, file):
        self.file = file
        self.content = ""

    def write(self, string):
        self.content += string

    def save(self):
        return Memento(self.file, self.content)

    def undo(self, memento):
        self.file = memento.file
        self.content = memento.content

class FileWriterCaretaker:
    def __init__(self):
        self.history = []

    def save(self, writer):
        if len(self.history) == 4:
            self.history.pop(0)  # Mantener máximo 4
        self.history.append(writer.save())

    def undo(self, writer, index=0):
        if 0 <= index < len(self.history):
            memento = self.history[-1 - index]
            writer.undo(memento)
        else:
            print(f"No hay un estado guardado para el índice {index}")

if __name__ == '__main__':
    os.system("clear")
    print("Crea un objeto que gestionará hasta 4 versiones anteriores")
    caretaker = FileWriterCaretaker()

    print("Crea el objeto cuyo estado se quiere preservar")
    writer = FileWriterUtility("GFG.txt")

    print("Se graba contenido A y se salva")
    writer.write("A\n")
    print(writer.content)
    caretaker.save(writer)

    print("Se graba contenido B y se salva")
    writer.write("B\n")
    print(writer.content)
    caretaker.save(writer)

    print("Se graba contenido C y se salva")
    writer.write("C\n")
    print(writer.content)
    caretaker.save(writer)

    print("Se graba contenido D y se salva")
    writer.write("D\n")
    print(writer.content)
    caretaker.save(writer)

    print("Se graba contenido E (no se guarda)")
    writer.write("E\n")
    print(writer.content)

    print("Undo índice 0 (último guardado)")
    caretaker.undo(writer, 0)
    print(writer.content)

    print("Undo índice 2 (tercer estado más reciente)")
    caretaker.undo(writer, 2)
    print(writer.content)

    print("Undo índice 3 (más antiguo, si existe)")
    caretaker.undo(writer, 3)
    print(writer.content)
