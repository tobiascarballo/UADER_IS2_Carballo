import json
import sys

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

# Pruebas
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python ejerC.py <token>")
        sys.exit(1)

    key = sys.argv[1]
    tm = TokenManager()
    print(f"Clave de {key}: {tm.get_token(key)}")