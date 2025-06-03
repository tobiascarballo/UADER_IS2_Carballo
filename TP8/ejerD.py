import json
from abc import ABC, abstractmethod

# patron singleton para acceder a las claves de los tokens
class TokenManager:
    _instance = None

    def __new__(cls, filepath='sitedata.json'):
        if cls._instance is None:
            cls._instance = super(TokenManager, cls).__new__(cls)
            cls._instance._load_tokens(filepath)
        return cls._instance

    def _load_tokens(self, filepath):
        try:
            with open(filepath, 'r') as f:
                self.tokens = json.load(f)
        except Exception as e:
            print(f"Error cargando archivo JSON: {e}")
            self.tokens = {}

    def get_token(self, key):
        return self.tokens.get(key, "Token no encontrado")

# patron chain of responsability

class PaymentHandler(ABC):
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler  # permite encadenamiento fluido

    @abstractmethod
    def handle(self, pedido_id, monto):
        pass

class Token1Handler(PaymentHandler):
    def __init__(self, saldo_inicial=1000):
        super().__init__()
        self.saldo = saldo_inicial
        self.token_name = "token1"

    def handle(self, pedido_id, monto):
        if self.saldo >= monto:
            self.saldo -= monto
            return {
                "pedido": pedido_id,
                "token": self.token_name,
                "monto": monto
            }
        elif self._next_handler:
            return self._next_handler.handle(pedido_id, monto)
        else:
            return {"error": f"Saldo insuficiente para el pedido {pedido_id}"}

class Token2Handler(PaymentHandler):
    def __init__(self, saldo_inicial=2000):
        super().__init__()
        self.saldo = saldo_inicial
        self.token_name = "token2"

    def handle(self, pedido_id, monto):
        if self.saldo >= monto:
            self.saldo -= monto
            return {
                "pedido": pedido_id,
                "token": self.token_name,
                "monto": monto
            }
        elif self._next_handler:
            return self._next_handler.handle(pedido_id, monto)
        else:
            return {"error": f"Saldo insuficiente para el pedido {pedido_id}"}

# clase que gestiona los pagos automaticos

class PaymentProcessor:
    def __init__(self):
        self.token1 = Token1Handler()
        self.token2 = Token2Handler()
        self.token1.set_next(self.token2)  # cadena: token1 a token2
        self.token2.set_next(self.token1)  # para permitir alternancia
        self.handlers = [self.token1, self.token2]
        self.next_index = 0
        self.pagos = []  # para registrar los pagos realizados

    def procesar_pago(self, pedido_id, monto):
        handler = self.handlers[self.next_index]
        resultado = handler.handle(pedido_id, monto)
        self.next_index = (self.next_index + 1) % 2  # alternar entre 0 y 1

        if "error" not in resultado:
            self.pagos.append(resultado)
        return resultado


#parte de prueba

if __name__ == '__main__':
    print("= TEST DE PAGO AUTOMÁTICO =")
    processor = PaymentProcessor()

    # simula 6 pagos de $500
    for i in range(1, 7):
        resultado = processor.procesar_pago(pedido_id=i, monto=500)
        print(resultado)
