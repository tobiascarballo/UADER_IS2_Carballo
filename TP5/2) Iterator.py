class Palabra:
    def __init__(self, texto):
        self.texto = texto

    def __iter__(self):
        return IteradorDirecto(self.texto)

    def iterar_reverso(self):
        return IteradorReverso(self.texto)


class IteradorDirecto:
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0

    def __next__(self):
        if self.pos < len(self.texto):
            caracter = self.texto[self.pos]
            self.pos += 1
            return caracter
        else:
            raise StopIteration

    def __iter__(self):
        return self


class IteradorReverso:
    def __init__(self, texto):
        self.texto = texto
        self.pos = len(texto) - 1

    def __next__(self):
        if self.pos >= 0:
            caracter = self.texto[self.pos]
            self.pos -= 1
            return caracter
        else:
            raise StopIteration

    def __iter__(self):
        return self


# Simulación
palabra = Palabra("AUTO")

print("Directo:", end=" ")
for letra in palabra:
    print(letra, end=" ")

print("\nReverso:", end=" ")
for letra in palabra.iterar_reverso():
    print(letra, end=" ")
