class Ping:
    def execute(self, ip):
        if not ip.startswith("192."):
            print(f"Acceso denegado a la IP {ip}. Solo se permiten IPs que comiencen con 192.")
            return
        print(f"Haciendo ping a {ip} (10 intentos):")
        for i in range(1, 11):
            print(f"Ping {i} a {ip}")

    def executefree(self, ip):
        print(f"Haciendo ping libre a {ip} (10 intentos):")
        for i in range(1, 11):
            print(f"Ping {i} a {ip}")

class PingProxy:
    def __init__(self):
        self.ping = Ping()

    def execute(self, ip):
        if ip == "192.168.0.254":
            print("Redirigiendo ping a www.google.com por política especial...")
            self.ping.executefree("www.google.com")
        else:
            self.ping.execute(ip)

# --- Prueba ---
if __name__ == "__main__":
    proxy = PingProxy()

    print("1. IP válida (192.168.1.1):")
    proxy.execute("192.168.1.1")

    print("\n2. IP bloqueada (10.0.0.1):")
    proxy.execute("10.0.0.1")

    print("\n3. IP especial (192.168.0.254):")
    proxy.execute("192.168.0.254")
