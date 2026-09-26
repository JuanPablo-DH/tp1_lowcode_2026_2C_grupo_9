import json

class Archivador:

    @staticmethod
    def cargar_json(ruta_archivo: str) -> list[dict]:
        """
        Carga y devuelve los datos de cualquier archivo JSON como una lista de diccionarios.
        Es genérico y sirve para cualquier tipo de dato.
        """
        try:
            with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                return datos
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo '{ruta_archivo}' no existe.")
        except json.JSONDecodeError as e:
            raise ValueError(f"El archivo JSON tiene un formato o sintaxis inválida: {e}")
        except Exception as e:
            raise IOError(f"Error al leer el archivo JSON: {e}")

    @staticmethod
    def guardar_json(ruta_archivo: str, datos: list[dict]) -> None:
        """
        Guarda cualquier lista de diccionarios en un archivo JSON con formato legible.
        """
        try:
            with open(ruta_archivo, mode="w", encoding="utf-8") as archivo:
                # indent=4 le da formato prolijo con sangría en el archivo .json
                # ensure_ascii=False permite guardar tildes y caracteres en español
                json.dump(datos, archivo, ensure_ascii=False, indent=4)
        except Exception as e:
            raise IOError(f"Error al guardar los datos en el archivo JSON: {e}")