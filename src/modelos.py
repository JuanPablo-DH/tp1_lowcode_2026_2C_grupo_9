# La clase Producto se enfoca en estructurar la informacion de cada Producto
class Producto:
    def __init__(
        self,
        id_producto: int,
        nombre: str,
        categoria: str,
        stock_actual: int,
        stock_minimo: int,
        precio_costo: float,
        precio_venta: float,
        proveedor: str
    ):
        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.precio_costo = precio_costo
        self.precio_venta = precio_venta
        self.proveedor = proveedor

    #region Getters y Setters

    @property
    def id_producto(self) -> int:
        return self._id_producto

    @id_producto.setter
    def id_producto(self, valor: int):
        self._id_producto = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        self._nombre = valor

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str):
        self._categoria = valor

    @property
    def stock_actual(self) -> int:
        return self._stock_actual

    @stock_actual.setter
    def stock_actual(self, valor: int):
        if valor < 0:
            raise ValueError("El stock actual no puede ser negativo.")
        self._stock_actual = valor

    @property
    def stock_minimo(self) -> int:
        return self._stock_minimo

    @stock_minimo.setter
    def stock_minimo(self, valor: int):
        if valor < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")
        self._stock_minimo = valor

    @property
    def precio_costo(self) -> float:
        return self._precio_costo

    @precio_costo.setter
    def precio_costo(self, valor: float):
        if valor < 0:
            raise ValueError("El precio de costo no puede ser negativo.")
        self._precio_costo = valor

    @property
    def precio_venta(self) -> float:
        return self._precio_venta

    @precio_venta.setter
    def precio_venta(self, valor: float):
        if valor < 0:
            raise ValueError("El precio de venta no puede ser negativo.")
        self._precio_venta = valor

    @property
    def proveedor(self) -> str:
        return self._proveedor

    @proveedor.setter
    def proveedor(self, valor: str):
        self._proveedor = valor

    #endregion Getters y Setters

    def calcular_capital_total() -> float:
        pass # Stock actual * Precio costo

    def calcular_margen() -> float:
        pass # Precio venta - Precio costo

    def calcular_capital_inmovilizado() -> float:
        pass # Stock actual * Precio costo

    def requiere_reabastecimiento() -> bool:
        pass # Stock actual <= Stock minimo

# La clase Inventario se enfoca en gestionar los Productos
class Inventario:
    def __init__(self, lista_productos: list[Producto]):
        self.lista_productos = lista_productos

    #region Getters y Setters

    @property
    def lista_productos(self) -> list[Producto]:
        return self._lista_productos

    @lista_productos.setter
    def lista_productos(self, valor: list[Producto]):
        self._lista_productos = valor

    #endregion Getters y Setters

    #region CRUD

    # Los metodos del CRUD privados se enfocan en manipular la lista de productos
    def __agregar(self, producto: Producto) -> bool:
        pass

    def __modificar(self, producto: Producto) -> bool:
        pass

    def __eliminar(self, id_producto: int) -> bool:
        pass

    # Los metodos del CRUD publicos se enfocan en manejar los errores (lanzar excepciones) al intentar agregar, modificar o eliminar un producto
    def agregar_producto(self, producto: Producto) -> None:
        pass

    def modificar_producto(self, producto: Producto) -> None:
        pass

    def eliminar_producto(self, id_producto: int) -> None:
        pass

    def obtener_producto(self, id_producto: int) -> Producto | None:
        pass

    #endregion CRUD

    #region Funcionalidad

    def buscar_por_categoria(categoria: str) -> list[Producto]:
        pass

    def buscar_por_proveedor(proveedor: str) -> list[Producto]:
        pass # Este metodo con el de buscar_por_categoria se podria hacer en un solo metodo

    def filtrar_por_stock_critico() -> list[Producto]:
        pass

    def calcular_capital_total() -> float:
        pass

    def calcular_margen_potencial() -> float:
        pass

    # Es una funcionalidad extra para probar las alertas de reabastecimiento
    def simular_ventas(self) -> bool:
        pass

    #endregion Funcionalidad

# La clase Informe se enfoca en mostrar el reporte de estado del Inventario
class Informe:
    def __init__(self, inventario: Inventario):
        self.inventario = inventario

    #region Getters y Setters
    
    @property
    def inventario(self) -> Inventario:
        return self._inventario

    @inventario.setter
    def inventario(self, valor: Inventario):
        self._inventario = valor

    #endregion Getters y Setters

    def generar_reporte_general() -> str:
        pass # Prepara la tabla completa formateada para la consola

    def generar_reporte_alertas() -> str:
        pass # Muestra la lista de productos criticos (sin stock)

    def generar_reporte_financiero() -> str:
        pass # Muestra el capital inmovilizado y los margenes proyectados

    def generar_reporte_filtrado() -> str:
        pass # Prepara la tabla filtrada formateada para la consola

    def generar_reporte_busqueda() -> str:
        pass # Muestra producto buscado (por categoria o proveedor)