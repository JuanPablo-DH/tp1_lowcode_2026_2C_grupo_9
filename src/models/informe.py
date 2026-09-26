from src.models.inventario import Inventario
from src.models.producto import Producto
from src.services.dolar_api import DolarApi

class Informe:
    def __init__(self, inventario: Inventario):
        self.inventario = inventario

    # ==========================================
    # Getters y setters
    # ==========================================

    @property
    def inventario(self) -> Inventario:
        return self._inventario

    @inventario.setter
    def inventario(self, valor: Inventario):
        if not isinstance(valor, Inventario):
            raise TypeError("El atributo inventario debe ser una instancia de la clase Inventario.")
        self._inventario = valor

    # ==========================================
    # Método Auxiliar Interno de Formato
    # ==========================================

    def _formatear_tabla(self, productos: list[Producto]) -> str:
        """Método auxiliar interno para construir una tabla perfectamente alineada."""
        if not productos:
            return "No se encontraron productos para mostrar.\n"

        # Anchos fijos asignados a cada columna
        w_id = 6
        w_nom = 25
        w_cat = 15
        w_stk = 6
        w_min = 6
        w_cost = 15
        w_vent = 15
        w_prov = 15

        encabezado = (
            f"{'ID':<{w_id}} | {'Nombre':<{w_nom}} | {'Categoría':<{w_cat}} | "
            f"{'Stock':<{w_stk}} | {'Mínimo':<{w_min}} | {'P. Costo':<{w_cost}} | "
            f"{'P. Venta':<{w_vent}} | {'Proveedor':<{w_prov}}\n"
            + "-" * 115 + "\n"
        )
        
        filas = []
        for p in productos:
            alerta = " ⚠️" if p.requiere_reabastecimiento() else ""
            
            # Recortamos (truncamos) los textos para asegurar que no desborden la columna
            nombre_fmt = p.nombre[:w_nom]
            cat_fmt = p.categoria[:w_cat]
            prov_fmt = p.proveedor[:w_prov]
            costo_str = f"AR$ {p.precio_costo:,.2f}"
            venta_str = f"AR$ {p.precio_venta:,.2f}"

            filas.append(
                f"{p.id_producto:<{w_id}} | {nombre_fmt:<{w_nom}} | {cat_fmt:<{w_cat}} | "
                f"{p.stock_actual:>{w_stk}} | {p.stock_minimo:>{w_min}} | "
                f"{costo_str:>{w_cost}} | {venta_str:>{w_vent}} | {prov_fmt:<{w_prov}}{alerta}"
            )
        
        return encabezado + "\n".join(filas) + "\n"

    # ==========================================
    # Generación de Reportes Públicos
    # ==========================================

    def generar_reporte_general(self) -> str:
        """Prepara la tabla completa formateada con todos los productos del inventario."""
        reporte = "========================================================================================\n"
        reporte += "                                REPORTE GENERAL DE INVENTARIO                           \n"
        reporte += "========================================================================================\n"
        reporte += self._formatear_tabla(self._inventario.lista_productos)
        
        return reporte

    def generar_reporte_alertas(self) -> str:
        """Muestra la lista de productos críticos que están por debajo o igual al stock mínimo."""
        criticos = self._inventario.filtrar_por_stock_critico()
        
        reporte = "========================================================================================\n"
        reporte += "                           ⚠️  ALERTAS DE REABASTECIMIENTO NECESARIO                   \n"
        reporte += "========================================================================================\n"
        
        if not criticos:
            reporte += "✅ Todos los productos cuentan con stock suficiente por encima del mínimo requerido.\n"
        else:
            reporte += f"Se encontraron {len(criticos)} producto(s) en estado crítico:\n\n"
            reporte += self._formatear_tabla(criticos)
            
        return reporte

    def generar_reporte_financiero(self) -> str:
        """Muestra el capital inmovilizado y los márgenes de ganancia proyectados."""
        total_capital = self._inventario.calcular_capital_total()
        total_margen = self._inventario.calcular_margen_potencial()
        total_productos = len(self._inventario.lista_productos)
        total_unidades = sum(p.stock_actual for p in self._inventario.lista_productos)

        reporte = "========================================================================================\n"
        reporte += "                                REPORTE FINANCIERO DE STOCK                             \n"
        reporte += "========================================================================================\n"

        # Anchos fijos para etiquetas y valores
        w_lbl = 38
        w_val = 20

        reporte += f" • {'Total de productos en catálogo:':<{w_lbl}} {f'{total_productos} catálogo(s)':>{w_val}}\n"
        reporte += f" • {'Total de unidades físicas en stock:':<{w_lbl}} {f'{total_unidades} unidad(es)':>{w_val}}\n"
        reporte += f" • {'Capital inmovilizado total (costo):':<{w_lbl}} {f'AR$ {total_capital:,.2f}':>{w_val}}\n"
        reporte += f" • {'Margen potencial de ganancia:':<{w_lbl}} {f'AR$ {total_margen:,.2f}':>{w_val}}\n"
        reporte += f" • {'Valor estimado a precio de venta:':<{w_lbl}} {f'AR$ {(total_capital + total_margen):,.2f}':>{w_val}}\n"
        reporte += "========================================================================================\n"

        return reporte

    def generar_reporte_filtrado(self, productos: list[Producto], titulo: str = "REPORTE FILTRADO") -> str:
        """Prepara una tabla formateada para una lista de productos previamente filtrada."""
        reporte = "========================================================================================\n"
        reporte += f"                                {titulo.upper():^56}\n"
        reporte += "========================================================================================\n"
        reporte += self._formatear_tabla(productos)

        return reporte

    def generar_reporte_busqueda(self, criterio: str, valor: str) -> str:
        """Busca productos por categoría o proveedor y devuelve el reporte formateado."""
        resultados = self._inventario.filtrar_por_criterio(criterio, valor)
        titulo = f"RESULTADOS DE BÚSQUEDA ({criterio.upper()}: '{valor}')"

        return self.generar_reporte_filtrado(resultados, titulo)

    def generar_reporte_transacciones(self) -> str:
        """Muestra la tabla del historial de transacciones (Ventas, Reposiciones y Actualizaciones)."""
        txs = self._inventario.lista_transacciones

        if not txs:
            return "No hay transacciones registradas hasta el momento.\n"

        # Anchos fijos asignados a cada columna
        w_id = 5
        w_tip = 13
        w_fec = 19
        w_pro = 22
        w_can = 6
        w_mon = 13
        w_det = 15

        reporte = "====================================================================================================\n"
        reporte += "                                HISTORIAL AUDITABLE DE TRANSACCIONES                                \n"
        reporte += "====================================================================================================\n"
        reporte += f"{'ID':<{w_id}} | {'Tipo':<{w_tip}} | {'Fecha/Hora':<{w_fec}} | {'Producto':<{w_pro}} | {'Cant.':<{w_can}} | {'Monto (AR$)':>{w_mon}} | {'Detalle':<{w_det}}\n"
        reporte += "-" * 100 + "\n"

        for t in txs:
            reporte += (
                f"{t.id_transaccion:<{w_id}} | {t.tipo:<{w_tip}} | {t.fecha:<{w_fec}} | {t.nombre_producto[:22]:<{w_pro}} | "
                f"{t.cantidad:<{w_can}} | AR$ {t.monto_total:>{w_mon},.2f} | {t.detalle[:15]:<{w_det}}\n"
            )
        
        return reporte

    def generar_reporte_costo_reposicion(self) -> str:
        """
        Calcula y muestra el costo total necesario para reabastecer 
        todos los productos que están por debajo de su stock mínimo.
        """
        # Filtrar solo los productos que requieren reabastecimiento
        criticos = [p for p in self._inventario.lista_productos if p.requiere_reabastecimiento()]

        if not criticos:
            return "✅ Todos los productos cuentan con stock suficiente. No se requiere reposición.\n"

        # Anchos de columna
        w_id = 6
        w_nom = 25
        w_stk = 6
        w_min = 6
        w_falt = 8
        w_cost = 15
        w_subt = 17

        reporte = (
            "========================================================================================\n"
            "                              REPORTE DE COSTO DE REPOSICIÓN                            \n"
            "========================================================================================\n"
            f"{'ID':<{w_id}} | {'Nombre':<{w_nom}} | {'Stock':<{w_stk}} | {'Mínimo':<{w_min}} | "
            f"{'Faltante':>{w_falt}} | {'P. Costo':>{w_cost}} | {'Subtotal Rep.':>{w_subt}}\n"
            + "-" * 92 + "\n"
        )

        costo_total_reposicion = 0.0
        total_unidades_faltantes = 0

        for p in criticos:
            cant_faltante = p.stock_minimo - p.stock_actual
            subtotal = cant_faltante * p.precio_costo

            costo_total_reposicion += subtotal
            total_unidades_faltantes += cant_faltante

            # Truncado de texto y formateo monetario alineado a la derecha
            nombre_fmt = p.nombre[:w_nom]
            costo_str = f"AR$ {p.precio_costo:,.2f}"
            subtotal_str = f"AR$ {subtotal:,.2f}"

            reporte += (
                f"{p.id_producto:<{w_id}} | {nombre_fmt:<{w_nom}} | {p.stock_actual:<{w_stk}} | "
                f"{p.stock_minimo:<{w_min}} | {cant_faltante:>{w_falt}} | "
                f"{costo_str:>{w_cost}} | {subtotal_str:>{w_subt}}\n"
            )

        reporte += "-" * 92 + "\n"
        reporte += f"📦 Total de unidades a comprar : {total_unidades_faltantes} unidad(es)\n"
        reporte += f"💰 Costo total de reposición   : AR$ {costo_total_reposicion:,.2f}\n"
        reporte += "========================================================================================\n"

        return reporte

    def generar_reporte_conversion_dolar(self, tipo_dolar: str = "oficial") -> str:
        """
        Consulta el precio del dólar en tiempo real mediante DolarApi y
        convierte la valuación total del inventario, costo de reposición y
        margen potencial de ganancia a USD.
        """
        cotizacion_data = DolarApi.obtener_cotizacion(tipo_dolar)

        if not cotizacion_data:
            return "❌ No se pudo obtener la cotización del dólar en tiempo real. Verifique su conexión a internet.\n"

        precio_venta_usd = cotizacion_data.get("venta", 0.0)
        precio_compra_usd = cotizacion_data.get("compra", 0.0)
        fecha_act = cotizacion_data.get("fechaActualizacion", "N/A")
        nombre_dolar = cotizacion_data.get("nombre", tipo_dolar.capitalize())

        if precio_venta_usd <= 0:
            return "❌ Cotización obtenida no válida para realizar la conversión.\n"

        # Totales del inventario en ARS
        total_valor_venta_ars = sum(p.stock_actual * p.precio_venta for p in self._inventario.lista_productos)
        total_costo_ars = sum(p.stock_actual * p.precio_costo for p in self._inventario.lista_productos)
        
        # Ganancia potencial y margen relativo (%) en ARS
        ganancia_potencial_ars = total_valor_venta_ars - total_costo_ars
        margen_porcentaje = (ganancia_potencial_ars / total_costo_ars * 100) if total_costo_ars > 0 else 0.0

        # Conversión a USD según precio de venta
        total_valor_venta_usd = total_valor_venta_ars / precio_venta_usd
        total_costo_usd = total_costo_ars / precio_venta_usd
        ganancia_potencial_usd = ganancia_potencial_ars / precio_venta_usd

        # Formatear la fecha para la visualización
        fecha_fmt = fecha_act[:19].replace("T", " ")

        # Anchos fijos para la sección de cotización (líneas simples)
        w_lbl_top = 36
        w_val_top = 47

        # Anchos fijos para las secciones de doble moneda (AR$ | U$D)
        w_lbl = 34
        w_ars = 22
        w_usd = 22

        reporte = "========================================================================================\n"
        reporte += f"                     VALUACIÓN DE INVENTARIO EN DÓLARES ({nombre_dolar.upper()})        \n"
        reporte += "========================================================================================\n"

        # Sección Superior: Cotización y Fecha
        reporte += f" 💵 {'Cotización dólar venta:':<{w_lbl_top}} {f'AR$ {precio_venta_usd:,.2f}':>{w_val_top}}\n"
        reporte += f" 💵 {'Cotización dólar compra:':<{w_lbl_top}} {f'AR$ {precio_compra_usd:,.2f}':>{w_val_top}}\n"
        reporte += f" 🕒 {'Última actualización API:':<{w_lbl_top}} {f'{fecha_fmt}':>{w_val_top}}\n"
        reporte += "-" * 88 + "\n"

        # Sección Principal: Valuación y Costos
        reporte += f" 📦 {'Valuación total venta:':<{w_lbl}} {f'AR$ {total_valor_venta_ars:,.2f}':>{w_ars}}  |  {f'U$D {total_valor_venta_usd:,.2f}':>{w_usd}}\n"
        reporte += f" 📦 {'Costo total de inversión:':<{w_lbl}} {f'AR$ {total_costo_ars:,.2f}':>{w_ars}}  |  {f'U$D {total_costo_usd:,.2f}':>{w_usd}}\n"
        reporte += "-" * 88 + "\n"

        # Sección Final: Margen de Ganancia
        margen_usd_str = f"U$D {ganancia_potencial_usd:,.2f} ({margen_porcentaje:.1f}%)"
        reporte += f" 📈 {'Margen potencial de ganancia:':<{w_lbl}} {f'AR$ {ganancia_potencial_ars:,.2f}':>{w_ars}}  |  {margen_usd_str:>{w_usd}}\n"
        reporte += "========================================================================================\n"

        return reporte
