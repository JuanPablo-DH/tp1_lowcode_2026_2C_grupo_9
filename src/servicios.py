from modelos import Producto

class Archivador:
    
    # Para manejar los errores, lanzar excepciones
    
    @staticmethod
    def cargar_csv(ruta_archivo: str) -> list[Producto] | None:
        pass # Crear la lista de productos desde el archivo "data/raw/datos.json"

    @staticmethod
    def guardar_csv(ruta_archivo: str, lista_productos: list[Producto]) -> None:
        pass # Guardar la lista de productos en el archivo "data/raw/datos.json"