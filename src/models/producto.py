class Producto:
    def __init__(
        self,
        id_producto: int = 1,
        nombre: str = "Borrador",
        categoria: str = "General",
        stock_actual: int = 0,
        stock_minimo: int = 0,
        precio_costo: float = 0.0,
        precio_venta: float = 0.0,
        proveedor: str = "General"
    ):
        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.precio_costo = precio_costo
        self.precio_venta = precio_venta
        self.proveedor = proveedor

    # ==========================================
    # Getters y setters
    # ==========================================

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
        if not valor or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("La categoría no puede estar vacía.")
        self._categoria = valor.strip()

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
        if not valor or not valor.strip():
            raise ValueError("El proveedor no puede estar vacío.")
        self._proveedor = valor.strip()

    # ==========================================
    # Métodos de Negocio / Cálculo
    # ==========================================

    def calcular_capital_inmovilizado(self) -> float:
        """
        Calcula el monto total invertido en el stock disponible de este producto
        (Stock actual * Precio de costo).
        """
        return float(self._stock_actual * self._precio_costo)

    def calcular_margen_unitario(self) -> float:
        """
        Calcula la ganancia unitaria bruta por cada venta del producto
        (Precio de venta - Precio de costo).
        """
        return float(self._precio_venta - self._precio_costo)

    def calcular_margen_total_potencial(self) -> float:
        """
        Calcula la ganancia total proyectada si se vendieran todas las unidades disponibles
        ((Precio de venta - Precio de costo) * Stock actual).
        """
        return float(self.calcular_margen_unitario() * self._stock_actual)

    def requiere_reabastecimiento(self) -> bool:
        """
        Devuelve True si el stock actual cayó por debajo o igual al stock mínimo configurado.
        """
        return self._stock_actual <= self._stock_minimo

    # ==========================================
    # Métodos Utilitarios
    # ==========================================

    def __str__(self) -> str:
        alerta = " ⚠️ [STOCK CRÍTICO]" if self.requiere_reabastecimiento() else ""
        return (
            f"[{self._id_producto}] {self._nombre} ({self._categoria}) | "
            f"Stock: {self._stock_actual}/{self._stock_minimo} | "
            f"Costo: ${self._precio_costo:.2f} | Venta: ${self._precio_venta:.2f}{alerta}"
        )

    def to_dict(self) -> dict:
        """Convierte las propiedades del Producto a un diccionario para guardar en JSON."""
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "stock_actual": self.stock_actual,
            "stock_minimo": self.stock_minimo,
            "precio_costo": self.precio_costo,
            "precio_venta": self.precio_venta,
            "proveedor": self.proveedor,
        }

    @staticmethod
    def from_dict(data: dict) -> "Producto":
        """Crea una instancia de Producto desempaquetando el diccionario."""
        return Producto(**data)
