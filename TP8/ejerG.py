"""
Sistema de pagos automatico utilizando patrones de diseño:
    Singleton: para acceder a las claves de los bancos desde un JSON.
    Chain of Responsibility: para elegir automaticamente la cuenta que realizara un pago.
    Iterator: para recorrer el historial de pagos en orden cronológico.

Versión: 1.2
"""

import json


class BancoSingleton:
    """
    Singleton que accede a las claves de los bancos desde un archivo JSON.
    Solo se crea una instancia sin importar cuántas veces se lo instancie.
    """

    _instance = None

    def __new__(cls, json_file='sitedata.json'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_data(json_file)
        return cls._instance

    def _load_data(self, json_file):
        with open(json_file, 'r') as f:
            self.data = json.load(f)

    def get_clave(self, token):
        """
        Devuelve la clave correspondiente al token dado.
        """
        return self.data.get(token)


class Pago:
    """
    Representa un pago realizado.
    """

    def __init__(self, pedido, token, monto):
        self.pedido = pedido
        self.token = token
        self.monto = monto

    def __str__(self):
        return f'Pedido #{self.pedido} - Token: {self.token} - Monto: ${self.monto}'


class HistorialPagos:
    """
    Clase que almacena los pagos realizados y permite iterarlos en orden cronológico.
    """

    def __init__(self):
        self._pagos = []

    def agregar_pago(self, pago):
        self._pagos.append(pago)

    def __iter__(self):
        return iter(self._pagos)

    def listar(self):
        """
        Imprime todos los pagos en orden cronológico.
        """
        for pago in self:
            print(pago)


class ManejadorPago:
    """
    Clase abstracta para implementar el patrón Chain of Responsibility.
    """

    def __init__(self):
        self.siguiente = None

    def establecer_siguiente(self, manejador):
        self.siguiente = manejador

    def manejar(self, pedido, monto):
        """
        Intenta manejar un pedido. Si no puede, lo pasa al siguiente.
        """
        raise NotImplementedError("Este método debe ser implementado por subclases.")


class CuentaBanco(ManejadorPago):
    """
    Clase que representa una cuenta de banco con saldo.
    """

    def __init__(self, token, saldo_inicial, historial):
        super().__init__()
        self.token = token
        self.saldo = saldo_inicial
        self.historial = historial
        self.singleton = BancoSingleton()

    def manejar(self, pedido, monto):
        if self.saldo >= monto:
            # se puede hacer el pago
            self.saldo -= monto
            clave = self.singleton.get_clave(self.token)
            pago = Pago(pedido, self.token, monto)
            self.historial.agregar_pago(pago)
            print(f'[OK] Pedido #{pedido} pagado con {self.token} (Clave: {clave})')
        elif self.siguiente:
            self.siguiente.manejar(pedido, monto)
        else:
            print(f'[ERROR] Pedido #{pedido} no pudo ser pagado (fondos insuficientes en todas las cuentas).')


def prueba_pagos():
    """
    Función de prueba automatica. Realiza 6 pagos de $500 alternando entre dos cuentas.
    """
    historial = HistorialPagos()

    # crear cuentas con saldo inicial
    cuenta1 = CuentaBanco('token1', 1000, historial)
    cuenta2 = CuentaBanco('token2', 2000, historial)

    # encadenar manejadores
    cuenta1.establecer_siguiente(cuenta2)
    cuenta2.establecer_siguiente(cuenta1)

    # realizar pagos automáticos
    print("= TEST DE PAGO AUTOMÁTICO =")
    for i in range(1, 7):  # pedidos 1 a 6
        cuenta1.manejar(i, 500)

    # mostrar historial final
    print("\n= HISTORIAL DE PAGOS =")
    historial.listar()


if __name__ == '__main__':
    prueba_pagos()
