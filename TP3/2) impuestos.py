# impuestos con patron singleton.py como guia

class CalculadoraImpuestos:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CalculadoraImpuestos, cls).__new__(cls)
        return cls._instance

    def calcular(self, base_imponible):
        if base_imponible < 0:
            raise ValueError("La base imponible debe ser no negativa")

        iva = base_imponible * 0.21
        iibb = base_imponible * 0.05
        contribuciones = base_imponible * 0.012

        total_impuestos = iva + iibb + contribuciones

        return {
            "iva": iva,
            "iibb": iibb,
            "contribuciones": contribuciones,
            "total": total_impuestos
        }


#parte interactiva del codigo
if __name__ == "__main__":
    try:
        base = float(input("Ingrese el importe base imponible: $"))
        calculadora = CalculadoraImpuestos()
        resultado = calculadora.calcular(base)

        print(f"\nDesglose de impuestos sobre          ${base:.2f}:")
        print(f"  - IVA (21%):                         ${resultado['iva']:.2f}")
        print(f"  - Ingresos Brutos (5%):              ${resultado['iibb']:.2f}")
        print(f"  - Contribuciones Municipales (1.2%): ${resultado['contribuciones']:.2f}")
        print(f"  * Total de impuestos:                ${resultado['total']:.2f}")
        print("")
        print(f"  Total a pagar (importe + impuestos): ${base + resultado['total']:.2f}")

    except ValueError as e:
        print("Error:", e)
