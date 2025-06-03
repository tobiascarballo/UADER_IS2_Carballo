import json


class TokenManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenManager, cls).__new__(cls)
            cls._instance._load_data()
        return cls._instance

    def _load_data(self):
        with open('sitedata.json', 'r') as f:
            self.tokens = json.load(f)
        self.saldos = {
            'token1': 1000,
            'token2': 2000
        }

    def get_token_key(self, token_name):
        return self.tokens.get(token_name)

    def get_saldo(self, token_name):
        return self.saldos.get(token_name, 0)

    def descontar(self, token_name, monto):
        if self.saldos.get(token_name, 0) >= monto:
            self.saldos[token_name] -= monto
            return True
        return False


class PaymentHandler:
    def __init__(self, token_name):
        self.token_name = token_name
        self.siguiente = None

    def set_next(self, handler):
        self.siguiente = handler

    def procesar(self, pedido_id, monto):
        manager = TokenManager()
        if manager.get_saldo(self.token_name) >= monto:
            manager.descontar(self.token_name, monto)
            return {
                'pedido': pedido_id,
                'token': self.token_name,
                'monto': monto
            }
        elif self.siguiente:
            return self.siguiente.procesar(pedido_id, monto)
        else:
            return {
                'pedido': pedido_id,
                'error': 'Fondos insuficientes en todas las cuentas'
            }


class Token1Handler(PaymentHandler):
    def __init__(self):
        super().__init__('token1')


class Token2Handler(PaymentHandler):
    def __init__(self):
        super().__init__('token2')


class PaymentIterator:
    def __init__(self, pagos):
        self._pagos = pagos
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._pagos):
            result = self._pagos[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration


class PaymentProcessor:
    def __init__(self):
        self.handler1 = Token1Handler()
        self.handler2 = Token2Handler()
        self.handler1.set_next(self.handler2)
        self.handler2.set_next(self.handler1)
        self.turno = True  # alternar
        self.pagos = []

    def procesar_pago(self, pedido_id, monto):
        handler = self.handler1 if self.turno else self.handler2
        self.turno = not self.turno
        resultado = handler.procesar(pedido_id, monto)
        if 'error' not in resultado:
            self.pagos.append(resultado)
        return resultado

    def __iter__(self):
        return PaymentIterator(self.pagos)

    def mostrar_listado(self):
        print("=== LISTADO DE PAGOS REALIZADOS ===")
        for pago in self:
            print(f"Pedido {pago['pedido']}: ${pago['monto']} pagado con {pago['token']}")


# prueba
if __name__ == '__main__':
    processor = PaymentProcessor()
    for i in range(1, 7):
        processor.procesar_pago(i, 500)

    processor.mostrar_listado()
