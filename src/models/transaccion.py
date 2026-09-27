from datetime import datetime

class Transaccion:
    TIPOS_PERMITIDOS = ["VENTA", "REABASTECER", "DESABASTECER", "ACTUALIZACION"]
    FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"

    def __init__(
        self,
        id_transaccion: int,
        tipo: str,
        id_producto: int,
        nombre_producto: str,
        cantidad: int,
        monto_total: float = 0.0,
        detalle: str = "",
        fecha: str = ""
    ):
        self.id_transaccion = id_transaccion
        self.tipo = tipo
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.cantidad = cantidad
        self.monto_total = monto_total
        self.detalle = detalle
        self.fecha = fecha

    # ==========================================
    # Getters y setters
    # ==========================================

    @property
    def id_transaccion(self) -> int:
        return self._id_transaccion

    @id_transaccion.setter
    def id_transaccion(self, valor: int):
        self._id_transaccion = valor

    @property
    def tipo(self) -> str:
        return self._tipo

    @tipo.setter
    def tipo(self, valor: str):
        valor_upper = valor.strip().upper()
        if valor_upper not in self.TIPOS_PERMITIDOS:
            raise ValueError(f"Tipo de transacción inválido. Debe ser uno de: {self.TIPOS_PERMITIDOS}")
        self._tipo = valor_upper

    @property
    def id_producto(self) -> int:
        return self._id_producto

    @id_producto.setter
    def id_producto(self, valor: int):
        self._id_producto = valor

    @property
    def nombre_producto(self) -> str:
        return self._nombre_producto

    @nombre_producto.setter
    def nombre_producto(self, valor: str):
        self._nombre_producto = valor.strip()

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int):
        self._cantidad = valor

    @property
    def monto_total(self) -> float:
        return self._monto_total

    @monto_total.setter
    def monto_total(self, valor: float):
        self._monto_total = valor
    
    @property
    def detalle(self) -> str:
        return self._detalle

    @detalle.setter
    def detalle(self, valor: str):
        self._detalle = valor.strip()

    @property
    def fecha(self) -> str:
        return self._fecha

    @fecha.setter
    def fecha(self, valor: str):
        # 1. Si viene vacío o None, asignamos la fecha y hora actual automáticamente
        if not valor or not valor.strip():
            self._fecha = datetime.now().strftime(self.FORMATO_FECHA)
            return

        # 2. Si viene un texto, validamos que respete el formato exacto
        try:
            valor_limpio = valor.strip()
            datetime.strptime(valor_limpio, self.FORMATO_FECHA)
            self._fecha = valor_limpio
        except ValueError:
            raise ValueError(
                f"Formato de fecha inválido: '{valor}'. Debe ser 'YYYY-MM-DD HH:MM:SS'."
            )

    # ==========================================
    # Métodos Utilitarios
    # ==========================================

    def to_dict(self) -> dict:
        """Convierte la transacción a un diccionario para guardar en JSON."""
        return {
            "id_transaccion": self.id_transaccion,
            "tipo": self.tipo,
            "id_producto": self.id_producto,
            "nombre_producto": self.nombre_producto,
            "cantidad": self.cantidad,
            "monto_total": self.monto_total,
            "detalle": self.detalle,
            "fecha": self.fecha
        }

    @classmethod
    def from_dict(cls, data: dict) -> Transaccion:
        """Instancia un objeto Transaccion desempaquetando un diccionario."""
        return cls(
            id_transaccion=data["id_transaccion"],
            tipo=data["tipo"],
            id_producto=data["id_producto"],
            nombre_producto=data["nombre_producto"],
            cantidad=data["cantidad"],
            monto_total=data.get("monto_total", 0.0),
            detalle=data.get("detalle", ""),
            fecha=data.get("fecha")
        )