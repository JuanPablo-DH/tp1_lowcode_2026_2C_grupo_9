# La clase Producto se enfoca en estructurar la informacion de cada Producto
class Producto:
    __id_producto: int
    __nombre: str
    __categoria: str
    __stock_actual: int
    __stock_minimo: int
    __precio_costo: float
    __precio_venta: float
    __proveedor: str

    #region Getters y Setters

    @property
    def __id_producto(self):
        return self.__id_producto
    
    @property
    def __nombre(self):
        return self.__nombre
    
    @property
    def __categoria(self):
        return self.__categoria

    @property
    def __stock_actual(self):
        return self.__stock_actual

    @property
    def __stock_minimo(self):
        return self.__stock_minimo

    @property
    def __precio_costo(self):
        return self.__precio_costo

    @property
    def __precio_venta(self):
        return self.__precio_venta

    @property
    def __proveedor(self):
        return self.__proveedor

    @__id_producto.setter
    def __id_producto(self, id_producto):
        self.__id_producto = id_producto

    @__nombre.setter
    def __nombre(self, id_producto):
        self.__nombre = id_producto

    @__categoria.setter
    def __categoria(self, id_producto):
        self.__categoria = id_producto

    @__stock_actual.setter
    def __stock_actual(self, id_producto):
        self.__stock_actual = id_producto

    @__stock_minimo.setter
    def __stock_minimo(self, id_producto):
        self.__stock_minimo = id_producto

    @__precio_costo.setter
    def __precio_costo(self, id_producto):
        self.__precio_costo = id_producto

    @__precio_venta.setter
    def __precio_venta(self, id_producto):
        self.__precio_venta = id_producto

    @__proveedor.setter
    def __proveedor(self, id_producto):
        self.__proveedor = id_producto

    #endregion Getters y Setters

    def __init__(
        self,
        id_producto,
        nombre,
        categoria,
        stock_actual,
        stock_minimo,
        precio_costo,
        precio_venta,
        proveedor):
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__categoria = categoria
        self.__stock_actual = stock_actual
        self.__stock_minimo = stock_minimo
        self.__precio_costo = precio_costo
        self.__precio_venta = precio_venta
        self.__proveedor = proveedor

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
    __lista_productos: list[Producto]

    # Agregar getter y setter

    def __init__(self):
        pass

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
        pass

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