import argparse
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

    def get_saldo(self, token_name):
        return self.saldos.get(token_name, 0)

    def descontar(self, token_name, monto):
        if self.saldos.get(token_name, 0) >= monto:
            self.saldos[token_name] -= monto
            return True
        return False


class PaymentHandler:
    def __init__(self, token_name, verbose=False):
        self.token_name = token_name
        self.siguiente = None
        self.verbose = verbose

    def set_next(self, handler):
        self.siguiente = handler

    def procesar(self, pedido_id, monto):
        manager = TokenManager()
        if self.verbose:
            print(f"[DEBUG] Intentando procesar pedido {pedido_id} con {self.token_name}, saldo: {manager.get_saldo(self.token_name)}")

        if manager.get_saldo(self.token_name) >= monto:
            manager.descontar(self.token_name, monto)
            if self.verbose:
                print(f"[DEBUG] Pago aceptado. Nuevo saldo: {manager.get_saldo(self.token_name)}")
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
    def __init__(self, verbose=False):
        super().__init__('token1', verbose)


class Token2Handler(PaymentHandler):
    def __init__(self, verbose=False):
        super().__init__('token2', verbose)


class PaymentProcessor:
    def __init__(self, verbose=False):
        self.handler1 = Token1Handler(verbose)
        self.handler2 = Token2Handler(verbose)
        self.handler1.set_next(self.handler2)
        self.handler2.set_next(self.handler1)
        self.turno = True
        self.pagos = []

    def procesar_pago(self, pedido_id, monto):
        handler = self.handler1 if self.turno else self.handler2
        self.turno = not self.turno
        resultado = handler.procesar(pedido_id, monto)
        if 'error' not in resultado:
            self.pagos.append(resultado)
        return resultado

    def mostrar_listado(self):
        print("= LISTADO DE PAGOS =")
        for pago in self.pagos:
            print(f"Pedido {pago['pedido']}: ${pago['monto']} con {pago['token']}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='Activa la salida de depuración')
    args = parser.parse_args()

    processor = PaymentProcessor(verbose=args.verbose)

    for i in range(1, 7):
        processor.procesar_pago(i, 500)

    processor.mostrar_listado()