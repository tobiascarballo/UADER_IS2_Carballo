class Handler:
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler  # Permite encadenar con fluidez

    def handle(self, number):
        if self._next_handler:
            self._next_handler.handle(number)
        else:
            print(f"{number}: No consumido")

class EvenNumberHandler(Handler):
    def handle(self, number):
        if number % 2 == 0:
            print(f"{number}: Consumido por EvenNumberHandler (número par)")
        else:
            super().handle(number)

class PrimeNumberHandler(Handler):
    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def handle(self, number):
        if self.is_prime(number):
            print(f"{number}: Consumido por PrimeNumberHandler (número primo)")
        else:
            super().handle(number)

class UnconsumedHandler(Handler):
    def handle(self, number):
        print(f"{number}: No consumido por ningún handler")


# Construcción de la cadena
prime_handler = PrimeNumberHandler()
even_handler = EvenNumberHandler()
unconsumed_handler = UnconsumedHandler()

prime_handler.set_next(even_handler).set_next(unconsumed_handler)

# Paso de los números del 1 al 100
for number in range(1, 101):
    prime_handler.handle(number)
