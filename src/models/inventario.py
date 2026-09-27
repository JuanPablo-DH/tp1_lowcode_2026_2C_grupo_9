import random
from src.models.producto import Producto
from src.models.transaccion import Transaccion
from src.services.archivador import Archivador

class Inventario:
    def __init__(self,
            lista_productos: list[Producto] = None,
            lista_transacciones: list[Transaccion] = None
    ):
        self.lista_productos = lista_productos
        self.lista_transacciones = lista_transacciones

    # ==========================================
    # Getters y setters
    # ==========================================

    @property
    def lista_productos(self) -> list[Producto]:
        return self._lista_productos

    @lista_productos.setter
    def lista_productos(self, valor: list[Producto]):
        self._lista_productos = valor if valor is not None else []

    @property
    def lista_transacciones(self) -> list[Transaccion]:
        return self._lista_transacciones

    @lista_transacciones.setter
    def lista_transacciones(self, valor: list[Transaccion]):
        self._lista_transacciones = valor if valor is not None else []

    # ==========================================
    # Métodos Utilitarios
    # ==========================================

    def obtener_producto(self, id_producto: int) -> Producto | None:
        """
        Busca un producto por su ID en la lista.
        Devuelve la instancia de Producto si lo encuentra, o None si no existe.
        """
        for producto in self._lista_productos:
            if producto.id_producto == id_producto:
                return producto
        return None

    def _registrar_transaccion(
        self, tipo: str, producto: Producto, cantidad: int, monto_total: float = 0.0, detalle: str = ""
    ) -> Transaccion:
        """Método auxiliar interno para registrar cualquier tipo de transacción."""
        id_nueva = len(self._lista_transacciones) + 1
        tx = Transaccion(
            id_transaccion=id_nueva,
            tipo=tipo,
            id_producto=producto.id_producto,
            nombre_producto=producto.nombre,
            cantidad=cantidad,
            monto_total=monto_total,
            detalle=detalle
        )
        self._lista_transacciones.append(tx)
        return tx

    # ==========================================
    # Métodos Privados del CRUD (Manipulación Directa)
    # Nota: Usamos un guion bajo '_' por convención estándar PEP 8
    # ==========================================

    def _agregar(self, producto: Producto) -> bool:
        """Agrega directamente el objeto Producto a la lista interna."""
        self._lista_productos.append(producto)
        return True

    def _modificar(self, producto: Producto) -> bool:
        """Reemplaza los datos del producto existente por los del nuevo objeto."""
        for i, p in enumerate(self._lista_productos):
            if p.id_producto == producto.id_producto:
                self._lista_productos[i] = producto
                return True
        return False

    def _eliminar(self, id_producto: int) -> bool:
        """Remueve el producto de la lista por su ID."""
        producto = self.obtener_producto(id_producto)
        if producto is not None:
            self._lista_productos.remove(producto)
            return True
        return False

    # ==========================================
    # Métodos Públicos del CRUD (Validaciones y Excepciones)
    # ==========================================

    def agregar_producto(self, producto: Producto) -> Transaccion:
        """Valida que el ID no esté duplicado, agrega el producto y registra la alta."""
        if self.obtener_producto(producto.id_producto) is not None:
            raise ValueError(f"Ya existe un producto registrado con el ID {producto.id_producto}.")
        
        self._agregar(producto)
        
        return self._registrar_transaccion(
            tipo="ACTUALIZACION",
            producto=producto,
            cantidad=producto.stock_actual,
            monto_total=producto.stock_actual * producto.precio_venta,
            detalle="Alta de producto"
        )

    def modificar_producto(self, producto: Producto) -> Transaccion:
        """Valida la existencia del producto, aplica los cambios y registra la actualización."""
        if self.obtener_producto(producto.id_producto) is None:
            raise ValueError(f"No se encontró ningún producto con el ID {producto.id_producto} para modificar.")
        
        self._modificar(producto)
        
        return self._registrar_transaccion(
            tipo="ACTUALIZACION",
            producto=producto,
            cantidad=producto.stock_actual,
            monto_total=0.0,
            detalle="Modificación de producto"
        )

    def eliminar_producto(self, producto: Producto) -> Transaccion:
        """Valida que el producto exista, registra la baja en transacciones y lo elimina del catálogo."""
        if self.obtener_producto(producto.id_producto) is None:
            raise ValueError(f"No se encontró ningún producto con el ID {producto.id_producto} para eliminar.")
        
        tx = self._registrar_transaccion(
            tipo="ACTUALIZACION",
            producto=producto,
            cantidad=producto.stock_actual,
            monto_total=0.0,
            detalle="Baja de producto"
        )
        
        self._eliminar(producto.id_producto)

        return tx

    def reabastecer_producto(self, id_producto: int, cantidad: int) -> Transaccion:
        """Suma stock a un producto y registra la transacción de tipo REPOSICION."""
        prod = self.obtener_producto(id_producto)
        if prod is None:
            raise ValueError(f"No existe el producto con ID {id_producto}.")
        
        prod.stock_actual += cantidad 

        return self._registrar_transaccion(
            tipo="REABASTECER",
            producto=prod,
            cantidad=cantidad,
            monto_total=cantidad * prod.precio_costo,
            detalle=f"Ingreso de stock (+{cantidad} u.)"
        )

    def desabastecer_producto(self, id_producto: int, cantidad: int) -> Transaccion:
        """
        Resta unidades al stock de un producto (retiro, merma o ajuste) y registra la transacción.
        Lanza ValueError si el producto no existe o si la cantidad supera el stock disponible.
        """
        prod = self.obtener_producto(id_producto)
        if prod is None:
            raise ValueError(f"No existe el producto con ID {id_producto}.")

        if cantidad <= 0:
            raise ValueError("La cantidad a descontar debe ser mayor a 0.")

        if cantidad > prod.stock_actual:
            raise ValueError(
                f"Stock insuficiente. Stock disponible: {prod.stock_actual} u., intentó retirar: {cantidad} u."
            )

        prod.stock_actual -= cantidad

        return self._registrar_transaccion(
            tipo="DESABASTECER",
            producto=prod,
            cantidad=cantidad,
            monto_total=cantidad * prod.precio_costo,
            detalle=f"Retiro de stock (-{cantidad} u.)"
        )


    # ==========================================
    # Búsquedas y Filtros
    # ==========================================

    def filtrar_por_criterio(self, atributo: str, valor: str) -> list[Producto]:
        """
        Método unificado para filtrar productos por cualquier atributo de texto
        (ej: 'categoria' o 'proveedor'), ignorando mayúsculas/minúsculas.
        """
        resultado = []
        valor_buscado = valor.strip().lower()

        for producto in self._lista_productos:
            # Obtiene dinámicamente el valor de la propiedad del producto (ej. producto.categoria)
            valor_atributo = str(getattr(producto, atributo, "")).strip().lower()
            if valor_buscado in valor_atributo:
                resultado.append(producto)

        return resultado

    def buscar_por_categoria(self, categoria: str) -> list[Producto]:
        """Filtra los productos pertenecientes a una categoría específica."""
        return self.filtrar_por_criterio("categoria", categoria)

    def buscar_por_proveedor(self, proveedor: str) -> list[Producto]:
        """Filtra los productos pertenecientes a un proveedor específico."""
        return self.filtrar_por_criterio("proveedor", proveedor)

    def filtrar_por_stock_critico(self) -> list[Producto]:
        """
        Devuelve la lista de productos cuyo stock actual es menor o igual
        al stock mínimo (utiliza el método del Producto).
        """
        return [p for p in self._lista_productos if p.requiere_reabastecimiento()]

    # ==========================================
    # Indicadores Financieros / Métricas
    # ==========================================

    def calcular_capital_total(self) -> float:
        """Calcula el costo total invertido en el stock disponible de todos los productos."""
        return sum(p.calcular_capital_inmovilizado() for p in self._lista_productos)

    def calcular_margen_potencial(self) -> float:
        """
        Calcula la ganancia total proyectada si se vendiera todo el stock disponible
        sumando el margen total potencial de cada producto registrado.
        """
        return sum(p.calcular_margen_total_potencial() for p in self._lista_productos)

    # ==========================================
    # Simulación de Ventas
    # ==========================================

    def simular_ventas(self) -> Transaccion | None:
        """Simula una venta, descuenta stock y registra la transacción de tipo VENTA."""
        productos_disponibles = [p for p in self._lista_productos if p.stock_actual > 0]
        
        if not productos_disponibles:
            return None

        # Elegir un producto al azar
        # Generar una cantidad a vender entre 1  y el total de stock_actual
        producto_elegido = random.choice(productos_disponibles)
        cantidad = random.randint(1, producto_elegido.stock_actual)
        
        producto_elegido.stock_actual -= cantidad
        
        return self._registrar_transaccion(
            tipo="VENTA",
            producto=producto_elegido,
            cantidad=cantidad,
            monto_total=cantidad * producto_elegido.precio_venta,
            detalle=f"Venta simulada de {cantidad} u."
        )

    # ==========================================
    # Persistencia de datos
    # ==========================================

    @staticmethod
    def _cargar_lista(ruta: str, funcion_conversion) -> list:
        """
        Método auxiliar genérico que lee un archivo JSON con el Archivador 
        y aplica una función de conversión (from_dict) a cada elemento.
        """
        datos = Archivador.cargar_json(ruta)
        
        return [funcion_conversion(d) for d in datos]

    @staticmethod
    def cargar_productos(ruta_productos: str) -> list[Producto]:
        """Lee el JSON de productos y devuelve la lista de objetos Producto."""
        return Inventario._cargar_lista(ruta_productos, Producto.from_dict)

    @staticmethod
    def cargar_transacciones(ruta_transacciones: str) -> list[Transaccion]:
        """Lee el JSON de transacciones y devuelve la lista de objetos Transaccion."""
        return Inventario._cargar_lista(ruta_transacciones, Transaccion.from_dict)

    @staticmethod
    def _guardar_lista(ruta: str, lista: list) -> int:
        """
        Convierte cada objeto de la lista a diccionario llamando a su método .to_dict()
        y lo guarda mediante el Archivador. Devuelve la cantidad de elementos guardados.
        """
        Archivador.guardar_json(ruta, [e.to_dict() for e in lista])

        return len(lista)

    def guardar_datos(self, ruta_productos: str, ruta_transacciones: str) -> tuple[int, int]:
        """
        Persiste los productos y el historial de transacciones en sus respectivos archivos JSON.
        Devuelve una tupla con (cantidad_productos, cantidad_transacciones).
        """
        cant_prod = self._guardar_lista(ruta_productos, self._lista_productos)
        cant_tx = self._guardar_lista(ruta_transacciones, self._lista_transacciones)

        return cant_prod, cant_tx
