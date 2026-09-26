from datetime import datetime

class Transaccion:
    TIPOS_PERMITIDOS = ["VENTA", "REPOSICION", "ACTUALIZACION"]

    def __init__(
        self,
        id_transaccion: int,
        tipo: str,
        id_producto: int,
        nombre_producto: str,
        cantidad: int,
        monto_total: float = 0.0,
        detalle: str = "",
        fecha: str = None
    ):
        self.id_transaccion = id_transaccion
        self.tipo = tipo
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.cantidad = cantidad
        self.monto_total = monto_total
        self.detalle = detalle
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def tipo(self) -> str:
        return self._tipo

    @tipo.setter
    def tipo(self, valor: str):
        valor_upper = valor.strip().upper()
        if valor_upper not in self.TIPOS_PERMITIDOS:
            raise ValueError(f"Tipo de transacción inválido. Debe ser uno de: {self.TIPOS_PERMITIDOS}")
        self._tipo = valor_upper

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