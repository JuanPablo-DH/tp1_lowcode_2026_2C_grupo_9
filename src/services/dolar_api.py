import urllib.request
import json

class DolarApi:
    BASE_URL = "https://dolarapi.com/v1/dolares"

    @classmethod
    def obtener_cotizacion(cls, tipo: str = "oficial") -> dict | None:
        """
        Consulta la API pública de DolarApi.com para obtener la cotización del dólar en tiempo real.
        Devuelve un diccionario con los datos o None en caso de error de red o timeout.
        """
        url = f"{cls.BASE_URL}/{tipo.lower()}"
        try:
            # Petición HTTP GET con User-Agent para evitar bloqueos
            req = urllib.request.Request(
                url, 
                headers={"User-Agent": "Mozilla/5.0 (Python App)"}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = response.read().decode("utf-8")
                    return json.loads(data)
        except Exception as e:
            print(f"⚠️ No se pudo conectar con DolarApi ({e}).")
            return None