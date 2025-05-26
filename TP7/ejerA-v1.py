import json

class JsonReader:
    """Clase para leer archivos JSON y obtener valores por clave."""
    
    def read_key_from_file(self, filename, key='token1'):
        """Lee el valor de una clave específica desde un archivo JSON."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data[key]
        except FileNotFoundError:
            return f"Error: archivo '{filename}' no encontrado."
        except KeyError:
            return f"Error: clave '{key}' no encontrada."
        except json.JSONDecodeError:
            return "Error: archivo JSON mal formado."
        except Exception as e:
            return f"Error inesperado: {str(e)}"
