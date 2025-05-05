# Componente base
class Componente:
    def mostrar(self, nivel=0):
        raise NotImplementedError("Método abstracto")

# Hoja (Leaf)
class Pieza(Componente):
    def __init__(self, nombre):
        self.nombre = nombre

    def mostrar(self, nivel=0):
        print("  " * nivel + f"Pieza: {self.nombre}")

# Compuesto (Composite)
class Conjunto(Componente):
    def __init__(self, nombre):
        self.nombre = nombre
        self.componentes = []

    def agregar(self, componente: Componente):
        self.componentes.append(componente)

    def mostrar(self, nivel=0):
        print("  " * nivel + f"Conjunto: {self.nombre}")
        for c in self.componentes:
            c.mostrar(nivel + 1)

if __name__ == "__main__":
    # Crear el producto principal
    producto_principal = Conjunto("Producto Principal")

    # Agregar tres subconjuntos, cada uno con cuatro piezas
    for i in range(1, 4):
        sub = Conjunto(f"Subconjunto {i}")
        for j in range(1, 5):
            sub.agregar(Pieza(f"P{i}{j}"))
        producto_principal.agregar(sub)

    # Mostrar jerarquía inicial
    print("== Configuración inicial ==")
    producto_principal.mostrar()

    # Agregar subconjunto adicional con 4 piezas
    adicional = Conjunto("Subconjunto Opcional")
    for j in range(1, 5):
        adicional.agregar(Pieza(f"O{j}"))
    producto_principal.agregar(adicional)

    print("\n== Configuración con subconjunto adicional ==")
    producto_principal.mostrar()
